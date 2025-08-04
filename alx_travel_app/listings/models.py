"""
Models for the listings app.

This module contains the database models for travel listings and related entities.
"""

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Listing(models.Model):
    """
    Model for travel listings available on the platform.
    """

    LISTING_TYPE_CHOICES = (
        ("hotel", "Hotel"),
        ("apartment", "Apartment"),
        ("villa", "Villa"),
        ("resort", "Resort"),
        ("hostel", "Hostel"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    description = models.TextField()
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    max_guests = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    featured_image = models.ImageField(
        upload_to="listings/%Y/%m/%d/", blank=True, null=True
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Listing"
        verbose_name_plural = "Listings"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ListingImage(models.Model):
    """
    Model for additional images associated with a listing.
    """

    listing = models.ForeignKey(
        Listing, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="listings/%Y/%m/%d/")
    caption = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Listing Image"
        verbose_name_plural = "Listing Images"

    def __str__(self):
        return f"Image for {self.listing.title}"


class Amenity(models.Model):
    """
    Model for amenities that can be associated with listings.
    """

    name = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=100, blank=True, help_text="Font awesome icon name"
    )

    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name


class ListingAmenity(models.Model):
    """
    Many-to-many relationship between listings and amenities.
    """

    listing = models.ForeignKey(
        Listing, related_name="listing_amenities", on_delete=models.CASCADE
    )
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("listing", "amenity")
        verbose_name = "Listing Amenity"
        verbose_name_plural = "Listing Amenities"

    def __str__(self):
        return f"{self.amenity.name} for {self.listing.title}"


class Booking(models.Model):
    """
    Model for user bookings of travel listings.
    """

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bookings"
    )
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_guests = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"Booking by {self.user.username} for {self.listing.title}"


class Review(models.Model):
    """
    Model for user reviews of travel listings.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="reviews"
    )
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="review",
        null=True,
        blank=True,
    )
    rating = models.PositiveIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)]
    )  # 1-5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        unique_together = ("user", "listing")  # One review per user per listing

    def __str__(self):
        return f"Review by {self.user.username} for {self.listing.title} - {self.rating} stars"


class Payment(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for {self.booking.id} - {self.status}"
