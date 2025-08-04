from django.contrib import admin
from .models import Listing, ListingImage, Amenity, ListingAmenity


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 3


class ListingAmenityInline(admin.TabularInline):
    model = ListingAmenity
    extra = 2


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "listing_type",
        "price_per_night",
        "location",
        "is_available",
        "created_at",
    )
    list_filter = (
        "listing_type",
        "is_available",
        "bedrooms",
        "bathrooms",
        "created_at",
    )
    search_fields = ("title", "description", "location", "address")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ListingImageInline, ListingAmenityInline]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "description",
                    "listing_type",
                    "featured_image",
                    "is_available",
                )
            },
        ),
        ("Pricing & Location", {"fields": ("price_per_night", "location", "address")}),
        ("Details", {"fields": ("max_guests", "bedrooms", "bathrooms")}),
    )


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")
    search_fields = ("name",)
