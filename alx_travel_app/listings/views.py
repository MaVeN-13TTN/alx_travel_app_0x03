"""
Views for the listings app.

This module contains the API views for travel listings and amenities.
"""

from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import QuerySet
from typing import Any
from .models import Listing, Amenity, Booking, Review, Payment
from .serializers import (
    ListingSerializer,
    AmenitySerializer,
    BookingSerializer,
    ReviewSerializer,
    PaymentSerializer,
)
from rest_framework.views import APIView
from chapa import Chapa
from django.conf import settings
import uuid
from django.shortcuts import get_object_or_404
from .tasks import send_payment_confirmation_email


class InitiatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)

        if booking.status == "confirmed":
            return Response(
                {"error": "This booking has already been paid for."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        transaction_id = str(uuid.uuid4())

        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            transaction_id=transaction_id,
            status="pending",
        )

        chapa = Chapa(settings.CHAPA_SECRET_KEY)

        payload = {
            "amount": str(booking.total_price),
            "currency": "ETB",
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "tx_ref": transaction_id,
            "callback_url": request.build_absolute_uri("/api/v1/payments/verify/"),
            "return_url": request.build_absolute_uri(
                f"/bookings/{booking.id}/confirmation/"
            ),
            "customization[title]": "Payment for Alx Travel",
            "customization[description]": f"Booking for {booking.listing.title}",
        }

        try:
            response = chapa.initialize(**payload)
            if response.get("status") == "success":
                return Response(
                    {"checkout_url": response["data"]["checkout_url"]},
                    status=status.HTTP_200_OK,
                )
            else:
                payment.status = "failed"
                payment.save()
                return Response(
                    {"error": "Could not initiate payment."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            payment.status = "failed"
            payment.save()
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyPaymentView(APIView):
    def get(self, request, *args, **kwargs):
        transaction_id = request.GET.get("tx_ref")

        if not transaction_id:
            return Response(
                {"error": "Transaction reference not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        chapa = Chapa(settings.CHAPA_SECRET_KEY)
        try:
            response = chapa.verify(transaction_id)
            if response.get("status") == "success":
                payment = get_object_or_404(Payment, transaction_id=transaction_id)
                payment.status = "completed"
                payment.save()

                booking = payment.booking
                booking.status = "confirmed"
                booking.save()

                # Trigger Celery task to send email
                send_payment_confirmation_email.delay(payment.id)

                return Response(
                    {"status": "Payment verified successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                payment = get_object_or_404(Payment, transaction_id=transaction_id)
                payment.status = "failed"
                payment.save()
                return Response(
                    {"error": "Payment verification failed."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for travel listings
    """

    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "listing_type",
        "is_available",
        "location",
        "max_guests",
        "bedrooms",
    ]
    search_fields = ["title", "description", "location", "address"]
    ordering_fields = ["price_per_night", "created_at", "bedrooms", "max_guests"]

    @action(detail=False)
    def featured(self, request):
        """Get featured listings"""
        featured = self.get_queryset().filter(is_available=True)[:5]
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)


class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for amenities
    """

    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for bookings
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "listing",
        "status",
        "check_in_date",
        "check_out_date",
        "user",
    ]
    ordering_fields = ["created_at", "check_in_date", "total_price"]
    ordering = ["-created_at"]

    def get_queryset(self) -> QuerySet[Booking]:  # type: ignore
        """Filter bookings by user for non-staff users"""
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user to the current user when creating a booking"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def my_bookings(self, request):
        """Get current user's bookings"""
        bookings = Booking.objects.filter(user=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def upcoming(self, request):
        """Get upcoming bookings for current user"""
        from datetime import date

        upcoming_bookings = Booking.objects.filter(
            user=request.user,
            check_in_date__gte=date.today(),
            status__in=["pending", "confirmed"],
        )
        serializer = self.get_serializer(upcoming_bookings, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint for reviews
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "listing",
        "user",
        "rating",
    ]
    ordering_fields = ["created_at", "rating"]
    ordering = ["-created_at"]

    def get_queryset(self) -> QuerySet[Review]:  # type: ignore
        """Filter reviews and allow users to edit only their own reviews"""
        queryset = Review.objects.all()

        # Filter by listing_id if specified in query params
        listing_id = getattr(self.request, "query_params", self.request.GET).get(  # type: ignore
            "listing_id", None
        )
        if listing_id is not None:
            queryset = queryset.filter(listing_id=listing_id)

        # For update/delete operations, non-staff users can only access their own reviews
        if self.action in ["update", "partial_update", "destroy"]:
            if not self.request.user.is_staff:
                queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        """Set the user to the current user when creating a review"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def my_reviews(self, request):
        """Get current user's reviews"""
        reviews = Review.objects.filter(user=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def top_rated(self, request):
        """Get top rated reviews (5 stars)"""
        top_reviews = Review.objects.filter(rating=5)[:10]
        serializer = self.get_serializer(top_reviews, many=True)
        return Response(serializer.data)
