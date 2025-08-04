"""
URL configuration for the listings app.

This module defines the URL patterns for the listings API endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"listings", views.ListingViewSet)
router.register(r"amenities", views.AmenityViewSet)
router.register(r"bookings", views.BookingViewSet)
router.register(r"reviews", views.ReviewViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "bookings/<int:booking_id>/pay/",
        views.InitiatePaymentView.as_view(),
        name="initiate-payment",
    ),
    path("payments/verify/", views.VerifyPaymentView.as_view(), name="verify-payment"),
]
