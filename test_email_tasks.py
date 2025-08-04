#!/usr/bin/env python
"""
Test script to verify Celery tasks are working properly.
"""
import os
import sys
import django

# Setup Django environment
sys.path.append("/home/meyvn/Desktop/ProDev-Backend/alx_travel_app_0x03/alx_travel_app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_travel_app.settings")
django.setup()

from listings.tasks import (
    send_booking_confirmation_email,
    send_payment_confirmation_email,
)
from listings.models import Booking, Payment, Listing, User
from datetime import date, timedelta
from decimal import Decimal


def test_booking_email_task():
    """Test the booking confirmation email task"""
    print("🧪 Testing booking confirmation email task...")

    # Try to create a test booking or use an existing one
    try:
        # Get or create test data
        user, created = User.objects.get_or_create(
            username="test_user",
            defaults={
                "email": "test@example.com",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        listing, created = Listing.objects.get_or_create(
            title="Test Listing",
            defaults={
                "slug": "test-listing",
                "description": "A test listing",
                "listing_type": "hotel",
                "price_per_night": Decimal("100.00"),
                "location": "Test City",
                "address": "123 Test St",
                "max_guests": 2,
                "bedrooms": 1,
                "bathrooms": 1,
            },
        )

        booking, created = Booking.objects.get_or_create(
            user=user,
            listing=listing,
            defaults={
                "check_in_date": date.today() + timedelta(days=7),
                "check_out_date": date.today() + timedelta(days=10),
                "num_guests": 2,
                "total_price": Decimal("300.00"),
                "status": "pending",
            },
        )

        print(f"📧 Queuing booking confirmation email for booking #{booking.id}")

        # Queue the task
        result = send_booking_confirmation_email.delay(booking.id)
        print(f"✅ Task queued successfully with ID: {result.id}")
        print(
            "📬 Email task has been sent to the queue. Start a Celery worker to process it."
        )

        return True

    except Exception as e:
        print(f"❌ Error testing booking email task: {e}")
        return False


def test_payment_email_task():
    """Test the payment confirmation email task"""
    print("\n🧪 Testing payment confirmation email task...")

    try:
        # Try to get an existing booking
        booking = Booking.objects.first()
        if not booking:
            print("❌ No bookings found. Create a booking first.")
            return False

        # Create or get a payment
        payment, created = Payment.objects.get_or_create(
            booking=booking,
            defaults={
                "amount": booking.total_price,
                "transaction_id": "test_transaction_123",
                "status": "completed",
            },
        )

        print(f"📧 Queuing payment confirmation email for payment #{payment.id}")

        # Queue the task
        result = send_payment_confirmation_email.delay(payment.id)
        print(f"✅ Task queued successfully with ID: {result.id}")
        print(
            "📬 Email task has been sent to the queue. Start a Celery worker to process it."
        )

        return True

    except Exception as e:
        print(f"❌ Error testing payment email task: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Testing Celery Email Tasks for ALX Travel App")
    print("=" * 50)

    # Test booking email
    booking_success = test_booking_email_task()

    # Test payment email
    payment_success = test_payment_email_task()

    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"  Booking Email Task: {'✅ PASS' if booking_success else '❌ FAIL'}")
    print(f"  Payment Email Task: {'✅ PASS' if payment_success else '❌ FAIL'}")

    if booking_success and payment_success:
        print("\n🎉 All tests passed! Celery tasks are working correctly.")
        print("\n📝 Next steps:")
        print(
            "1. Start a Celery worker: celery -A alx_travel_app worker --loglevel=info"
        )
        print("2. The worker will process the queued email tasks")
        print("3. Configure real email settings in .env for production")
    else:
        print("\n🚨 Some tests failed. Check the error messages above.")
