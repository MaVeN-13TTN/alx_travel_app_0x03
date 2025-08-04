#!/usr/bin/env python3
"""
ALX Travel App - API Demo Script
Demonstrates POST operations and CRUD functionality

This script shows how to interact with the API for creating and managing data.
"""

import requests
import json
from datetime import date, timedelta

BASE_URL = "http://localhost:8000/api"


def demo_api_operations():
    """Demonstrate API CRUD operations"""
    print("🚀 ALX Travel App - API CRUD Demo")
    print("=" * 50)

    # Test getting all listings
    print("\n🏠 Fetching all listings...")
    response = requests.get(f"{BASE_URL}/listings/")
    if response.status_code == 200:
        listings = response.json()
        print(f"✅ Found {len(listings)} listings")
        if listings:
            first_listing = listings[0]
            print(
                f"   Example: {first_listing['title']} - ${first_listing['price_per_night']}/night"
            )
    else:
        print(f"❌ Error: {response.status_code}")

    # Test filtering
    print("\n🔍 Testing filtering - Hotels only...")
    response = requests.get(f"{BASE_URL}/listings/?listing_type=hotel")
    if response.status_code == 200:
        hotels = response.json()
        print(f"✅ Found {len(hotels)} hotels")

    # Test search
    print("\n🔍 Testing search - Beach properties...")
    response = requests.get(f"{BASE_URL}/listings/?search=beach")
    if response.status_code == 200:
        beach_properties = response.json()
        print(f"✅ Found {len(beach_properties)} beach properties")

    # Test getting a specific listing
    print(f"\n🏠 Getting specific listing...")
    response = requests.get(f"{BASE_URL}/listings/luxury-beachfront-villa/")
    if response.status_code == 200:
        listing = response.json()
        print(f"✅ Retrieved: {listing['title']}")
        print(f"   Location: {listing['location']}")
        print(f"   Price: ${listing['price_per_night']}/night")
        print(f"   Guests: {listing['max_guests']}")
        print(f"   Amenities: {len(listing['amenities'])} available")

    # Test amenities
    print(f"\n🔧 Getting amenities...")
    response = requests.get(f"{BASE_URL}/amenities/")
    if response.status_code == 200:
        amenities = response.json()
        print(f"✅ Found {len(amenities)} amenities:")
        for amenity in amenities[:5]:  # Show first 5
            print(f"   - {amenity['name']} ({amenity['icon']})")
        if len(amenities) > 5:
            print(f"   ... and {len(amenities) - 5} more")

    # Test reviews
    print(f"\n⭐ Getting reviews...")
    response = requests.get(f"{BASE_URL}/reviews/")
    if response.status_code == 200:
        reviews = response.json()
        print(f"✅ Found {len(reviews)} reviews")
        if reviews:
            review = reviews[0]
            print(f"   Latest: {review['rating']}⭐ - \"{review['comment'][:50]}...\"")

    # Test top rated reviews
    print(f"\n⭐ Getting top rated reviews...")
    response = requests.get(f"{BASE_URL}/reviews/top_rated/")
    if response.status_code == 200:
        top_reviews = response.json()
        print(f"✅ Found {len(top_reviews)} 5-star reviews")

    # Test bookings (will require auth)
    print(f"\n📅 Testing bookings endpoint...")
    response = requests.get(f"{BASE_URL}/bookings/")
    if response.status_code == 403:
        print("✅ Bookings properly secured - authentication required")
    elif response.status_code == 200:
        print("✅ Bookings accessible (user authenticated)")
    else:
        print(f"❓ Unexpected status: {response.status_code}")

    print("\n" + "=" * 50)
    print("✅ API Demo Complete!")
    print(f"\n🌐 Try these URLs in your browser:")
    print(f"   • API Root: {BASE_URL}/")
    print(f"   • Swagger UI: http://localhost:8000/swagger/")
    print(f"   • ReDoc: http://localhost:8000/redoc/")
    print(f"\n📖 For authenticated endpoints, use Django admin or DRF browsable API")


if __name__ == "__main__":
    try:
        demo_api_operations()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API server")
        print("   Make sure Django server is running:")
        print("   python manage.py runserver")
    except Exception as e:
        print(f"❌ Error: {e}")
