"""
Management command to seed the database with sample data.

This command populates the database with sample listings, bookings, and reviews
for testing and development purposes.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Amenity, ListingAmenity, Booking, Review
from decimal import Decimal
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = "Seeds the database with sample data for listings, bookings, and reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--listings",
            type=int,
            default=10,
            help="Number of sample listings to create (default: 10)",
        )
        parser.add_argument(
            "--bookings",
            type=int,
            default=20,
            help="Number of sample bookings to create (default: 20)",
        )
        parser.add_argument(
            "--reviews",
            type=int,
            default=15,
            help="Number of sample reviews to create (default: 15)",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        # Create sample amenities first
        self.create_amenities()

        # Create sample users
        self.create_users()

        # Create sample listings
        listings_count = options["listings"]
        self.create_listings(listings_count)

        # Create sample bookings
        bookings_count = options["bookings"]
        self.create_bookings(bookings_count)

        # Create sample reviews
        reviews_count = options["reviews"]
        self.create_reviews(reviews_count)

        self.stdout.write(
            self.style.SUCCESS("Database seeding completed successfully!")
        )

    def create_amenities(self):
        """Create sample amenities."""
        amenities_data = [
            {"name": "WiFi", "icon": "fa-wifi"},
            {"name": "Swimming Pool", "icon": "fa-swimming-pool"},
            {"name": "Parking", "icon": "fa-parking"},
            {"name": "Air Conditioning", "icon": "fa-wind"},
            {"name": "Kitchen", "icon": "fa-utensils"},
            {"name": "Gym", "icon": "fa-dumbbell"},
            {"name": "Pet Friendly", "icon": "fa-paw"},
            {"name": "Balcony", "icon": "fa-city"},
            {"name": "Beach Access", "icon": "fa-umbrella-beach"},
            {"name": "Room Service", "icon": "fa-bell"},
        ]

        for amenity_data in amenities_data:
            amenity, created = Amenity.objects.get_or_create(
                name=amenity_data["name"], defaults={"icon": amenity_data["icon"]}
            )
            if created:
                self.stdout.write(f"Created amenity: {amenity.name}")

    def create_users(self):
        """Create sample users for bookings and reviews."""
        users_data = [
            {
                "username": "john_doe",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
            },
            {
                "username": "jane_smith",
                "email": "jane@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
            },
            {
                "username": "bob_wilson",
                "email": "bob@example.com",
                "first_name": "Bob",
                "last_name": "Wilson",
            },
            {
                "username": "alice_brown",
                "email": "alice@example.com",
                "first_name": "Alice",
                "last_name": "Brown",
            },
            {
                "username": "charlie_davis",
                "email": "charlie@example.com",
                "first_name": "Charlie",
                "last_name": "Davis",
            },
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={
                    "email": user_data["email"],
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                },
            )
            if created:
                user.set_password("password123")
                user.save()
                self.stdout.write(f"Created user: {user.username}")

    def create_listings(self, count):
        """Create sample listings."""
        sample_listings = [
            {
                "title": "Luxury Beachfront Villa",
                "description": "Beautiful villa with stunning ocean views and private beach access.",
                "listing_type": "villa",
                "price_per_night": Decimal("450.00"),
                "location": "Malibu, California",
                "address": "123 Ocean Drive, Malibu, CA 90265",
                "max_guests": 8,
                "bedrooms": 4,
                "bathrooms": 3,
            },
            {
                "title": "Cozy Downtown Apartment",
                "description": "Modern apartment in the heart of the city with all amenities.",
                "listing_type": "apartment",
                "price_per_night": Decimal("120.00"),
                "location": "New York, NY",
                "address": "456 Broadway, New York, NY 10013",
                "max_guests": 4,
                "bedrooms": 2,
                "bathrooms": 1,
            },
            {
                "title": "Mountain Resort Cabin",
                "description": "Peaceful cabin surrounded by mountains and nature trails.",
                "listing_type": "resort",
                "price_per_night": Decimal("200.00"),
                "location": "Aspen, Colorado",
                "address": "789 Mountain View Rd, Aspen, CO 81611",
                "max_guests": 6,
                "bedrooms": 3,
                "bathrooms": 2,
            },
            {
                "title": "Boutique Hotel Suite",
                "description": "Elegant hotel suite with premium services and city views.",
                "listing_type": "hotel",
                "price_per_night": Decimal("300.00"),
                "location": "San Francisco, CA",
                "address": "321 Union Square, San Francisco, CA 94108",
                "max_guests": 2,
                "bedrooms": 1,
                "bathrooms": 1,
            },
            {
                "title": "Budget-Friendly Hostel",
                "description": "Clean and safe hostel perfect for backpackers and solo travelers.",
                "listing_type": "hostel",
                "price_per_night": Decimal("35.00"),
                "location": "Portland, Oregon",
                "address": "654 SE Division St, Portland, OR 97202",
                "max_guests": 1,
                "bedrooms": 1,
                "bathrooms": 1,
            },
        ]

        # Create the predefined listings
        for listing_data in sample_listings[:count]:
            listing, created = Listing.objects.get_or_create(
                title=listing_data["title"], defaults=listing_data
            )
            if created:
                # Add random amenities to each listing
                amenities = Amenity.objects.all()
                random_amenities = random.sample(
                    list(amenities), k=random.randint(3, 6)
                )
                for amenity in random_amenities:
                    ListingAmenity.objects.get_or_create(
                        listing=listing, amenity=amenity
                    )
                self.stdout.write(f"Created listing: {listing.title}")

        # Create additional random listings if count > 5
        if count > 5:
            listing_types = ["hotel", "apartment", "villa", "resort", "hostel"]
            cities = [
                "Miami, FL",
                "Austin, TX",
                "Seattle, WA",
                "Boston, MA",
                "Chicago, IL",
                "Las Vegas, NV",
                "Atlanta, GA",
                "Denver, CO",
                "Phoenix, AZ",
                "Detroit, MI",
            ]

            for i in range(5, count):
                listing_type = random.choice(listing_types)
                city = random.choice(cities)

                listing_data = {
                    "title": f'{listing_type.title()} in {city.split(",")[0]} #{i+1}',
                    "description": f"A wonderful {listing_type} located in {city}.",
                    "listing_type": listing_type,
                    "price_per_night": Decimal(str(random.randint(50, 500))),
                    "location": city,
                    "address": f"{random.randint(100, 999)} Sample St, {city}",
                    "max_guests": random.randint(1, 8),
                    "bedrooms": random.randint(1, 4),
                    "bathrooms": random.randint(1, 3),
                }

                listing, created = Listing.objects.get_or_create(
                    title=listing_data["title"], defaults=listing_data
                )
                if created:
                    # Add random amenities
                    amenities = Amenity.objects.all()
                    random_amenities = random.sample(
                        list(amenities), k=random.randint(2, 5)
                    )
                    for amenity in random_amenities:
                        ListingAmenity.objects.get_or_create(
                            listing=listing, amenity=amenity
                        )
                    self.stdout.write(f"Created listing: {listing.title}")

    def create_bookings(self, count):
        """Create sample bookings."""
        users = list(User.objects.all())
        listings = list(Listing.objects.all())

        if not users or not listings:
            self.stdout.write(
                self.style.WARNING(
                    "No users or listings found. Skipping bookings creation."
                )
            )
            return

        statuses = ["pending", "confirmed", "cancelled", "completed"]

        for i in range(count):
            user = random.choice(users)
            listing = random.choice(listings)

            # Generate random dates
            start_date = date.today() + timedelta(days=random.randint(-30, 60))
            end_date = start_date + timedelta(days=random.randint(1, 14))

            # Calculate total price
            nights = (end_date - start_date).days
            total_price = listing.price_per_night * nights

            booking_data = {
                "user": user,
                "listing": listing,
                "check_in_date": start_date,
                "check_out_date": end_date,
                "num_guests": random.randint(1, listing.max_guests),
                "total_price": total_price,
                "status": random.choice(statuses),
            }

            booking, created = Booking.objects.get_or_create(
                user=user,
                listing=listing,
                check_in_date=start_date,
                defaults=booking_data,
            )
            if created:
                self.stdout.write(f"Created booking: {booking}")

    def create_reviews(self, count):
        """Create sample reviews."""
        users = list(User.objects.all())
        listings = list(Listing.objects.all())

        if not users or not listings:
            self.stdout.write(
                self.style.WARNING(
                    "No users or listings found. Skipping reviews creation."
                )
            )
            return

        sample_comments = [
            "Amazing place! Had a wonderful time and would definitely come back.",
            "Great location and very clean. The host was very responsive.",
            "Perfect for our family vacation. Kids loved the amenities.",
            "Beautiful views and peaceful atmosphere. Highly recommended!",
            "Good value for money. Everything was as described.",
            "The apartment was clean and well-equipped. Great location!",
            "Fantastic experience! The property exceeded our expectations.",
            "Very comfortable stay. The host provided excellent service.",
            "Beautiful property with great amenities. Will book again!",
            "Lovely place to stay. Very relaxing and peaceful environment.",
        ]

        created_reviews = set()

        for i in range(count):
            user = random.choice(users)
            listing = random.choice(listings)

            # Ensure unique user-listing combinations
            if (user.pk, listing.pk) in created_reviews:
                continue

            review_data = {
                "user": user,
                "listing": listing,
                "rating": random.randint(3, 5),  # Mostly positive reviews
                "comment": random.choice(sample_comments),
            }

            review, created = Review.objects.get_or_create(
                user=user, listing=listing, defaults=review_data
            )
            if created:
                created_reviews.add((user.pk, listing.pk))
                self.stdout.write(f"Created review: {review}")
