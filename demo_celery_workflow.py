#!/usr/bin/env python
"""
Comprehensive demo of Celery email functionality for ALX Travel App.
This script demonstrates the complete booking and email workflow.
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
import time


def create_demo_data():
    """Create demo data for testing"""
    print("📊 Creating demo data...")

    # Create test user
    user, created = User.objects.get_or_create(
        username="demo_user",
        defaults={
            "email": "demo@alxtravel.com",
            "first_name": "Demo",
            "last_name": "User",
        },
    )
    print(f"👤 User: {user.first_name} {user.last_name} ({user.email})")

    # Create test listing
    listing, created = Listing.objects.get_or_create(
        title="Luxury Beach Resort - Demo",
        defaults={
            "slug": "luxury-beach-resort-demo",
            "description": "A beautiful beach resort perfect for vacation",
            "listing_type": "resort",
            "price_per_night": Decimal("250.00"),
            "location": "Mombasa, Kenya",
            "address": "123 Beach Road, Mombasa",
            "max_guests": 4,
            "bedrooms": 2,
            "bathrooms": 2,
        },
    )
    print(f"🏨 Listing: {listing.title} - ETB {listing.price_per_night}/night")

    return user, listing


def demo_booking_workflow():
    """Demonstrate the complete booking workflow with emails"""
    print("\n🚀 DEMO: Booking Workflow with Email Notifications")
    print("=" * 60)

    # Create demo data
    user, listing = create_demo_data()

    # Step 1: Create a booking (this would trigger booking confirmation email)
    print("\n📅 Step 1: Creating a new booking...")
    booking = Booking.objects.create(
        user=user,
        listing=listing,
        check_in_date=date.today() + timedelta(days=14),
        check_out_date=date.today() + timedelta(days=17),
        num_guests=2,
        total_price=Decimal("750.00"),  # 3 nights × 250
        status="pending",
    )
    print(f"✅ Booking created: #{booking.id}")
    print(f"   📍 {booking.listing.title}")
    print(f"   📅 {booking.check_in_date} to {booking.check_out_date}")
    print(f"   👥 {booking.num_guests} guests")
    print(f"   💰 ETB {booking.total_price}")

    # Step 2: Send booking confirmation email (simulate BookingViewSet.perform_create)
    print("\n📧 Step 2: Sending booking confirmation email...")
    booking_task = send_booking_confirmation_email.delay(booking.id)
    print(f"✅ Booking email task queued: {booking_task.id}")

    # Step 3: Simulate payment processing
    print("\n💳 Step 3: Processing payment...")
    payment = Payment.objects.create(
        booking=booking,
        amount=booking.total_price,
        transaction_id=f"demo_txn_{int(time.time())}",
        status="completed",
    )

    # Update booking status
    booking.status = "confirmed"
    booking.save()

    print(f"✅ Payment processed: {payment.transaction_id}")
    print(f"   💰 Amount: ETB {payment.amount}")
    print(f"   📊 Status: {payment.status}")

    # Step 4: Send payment confirmation email (simulate VerifyPaymentView)
    print("\n📧 Step 4: Sending payment confirmation email...")
    payment_task = send_payment_confirmation_email.delay(payment.id)
    print(f"✅ Payment email task queued: {payment_task.id}")

    print("\n" + "=" * 60)
    print("🎉 Booking workflow complete!")
    print("\n📋 Summary:")
    print(f"   🆔 Booking ID: {booking.id}")
    print(f"   👤 Customer: {user.first_name} {user.last_name}")
    print(f"   📧 Email: {user.email}")
    print(f"   🏨 Property: {listing.title}")
    print(f"   💰 Total: ETB {booking.total_price}")
    print(f"   📊 Status: {booking.status}")

    print("\n📬 Email Tasks Queued:")
    print(f"   📧 Booking Confirmation: {booking_task.id}")
    print(f"   📧 Payment Confirmation: {payment_task.id}")

    return booking_task, payment_task


if __name__ == "__main__":
    print("🏖️  ALX TRAVEL APP - Celery Email Demo")
    print("=" * 60)
    print("This demo shows the complete booking workflow with email notifications")
    print("Emails will be displayed in the console when Celery worker processes them")

    # Run the demo
    booking_task, payment_task = demo_booking_workflow()

    print("\n🔧 To process these email tasks:")
    print("1. Open a new terminal")
    print(
        "2. Navigate to: cd /home/meyvn/Desktop/ProDev-Backend/alx_travel_app_0x03/alx_travel_app"
    )
    print("3. Activate venv: source ../venv/bin/activate")
    print("4. Start worker: celery -A alx_travel_app worker --loglevel=info")
    print("5. Watch the console for email output!")

    print("\n🌟 Features demonstrated:")
    print("  ✅ Automatic booking confirmation emails")
    print("  ✅ Payment confirmation emails")
    print("  ✅ Background task processing with Celery")
    print("  ✅ RabbitMQ message broker")
    print("  ✅ Django model integration")
    print("  ✅ Console email backend for development")
