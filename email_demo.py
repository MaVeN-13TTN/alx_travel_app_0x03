#!/usr/bin/env python
"""
Simple demonstration of email functionality.
This will process an email task synchronously to show the output.
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
from listings.models import Booking, Payment


def demonstrate_email_output():
    """Demonstrate email output by calling tasks directly"""
    print("📧 ALX Travel App - Email Functionality Demo")
    print("=" * 50)

    # Get bookings and payments
    booking = Booking.objects.first()
    payment = Payment.objects.first()

    if not booking:
        print("❌ No bookings found. Run demo_celery_workflow.py first.")
        return

    print(
        f"📋 Found booking #{booking.id} for {booking.user.first_name} {booking.user.last_name}"
    )
    print(f"🏨 Property: {booking.listing.title}")
    print(f"📧 Email: {booking.user.email}")

    print("\n" + "=" * 50)
    print("📬 BOOKING CONFIRMATION EMAIL")
    print("=" * 50)

    # Call booking email task directly (synchronously)
    try:
        result = send_booking_confirmation_email(booking.id)
        print(f"✅ Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")

    if payment:
        print("\n" + "=" * 50)
        print("💳 PAYMENT CONFIRMATION EMAIL")
        print("=" * 50)

        # Call payment email task directly (synchronously)
        try:
            result = send_payment_confirmation_email(payment.id)
            print(f"✅ Result: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")

    print("\n" + "=" * 50)
    print("🎉 Email Demo Complete!")
    print("\n💡 What you just saw:")
    print("  • Console email backend in action")
    print("  • Email content with booking/payment details")
    print("  • Background task functionality")
    print("\n🔧 For production:")
    print("  • Change EMAIL_BACKEND to smtp in settings.py")
    print("  • Configure real email credentials in .env")
    print("  • Start Celery worker to process tasks asynchronously")


if __name__ == "__main__":
    demonstrate_email_output()
