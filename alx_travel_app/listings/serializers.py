"""
Serializers for the listings app.

This module contains the DRF serializers for travel listings and amenities.
"""

from rest_framework import serializers
from .models import (
    Listing,
    ListingImage,
    Amenity,
    ListingAmenity,
    Booking,
    Review,
    Payment,
)
from django.contrib.auth.models import User


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ["id", "image", "caption"]


class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    amenities = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "listing_type",
            "price_per_night",
            "location",
            "address",
            "max_guests",
            "bedrooms",
            "bathrooms",
            "featured_image",
            "is_available",
            "created_at",
            "updated_at",
            "images",
            "amenities",
        ]

    def get_amenities(self, obj):
        amenity_items = ListingAmenity.objects.filter(listing=obj)
        return AmenitySerializer(
            [item.amenity for item in amenity_items], many=True
        ).data


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "listing",
            "listing_id",
            "check_in_date",
            "check_out_date",
            "num_guests",
            "total_price",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "total_price", "created_at", "updated_at"]


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "listing",
            "listing_id",
            "booking",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
