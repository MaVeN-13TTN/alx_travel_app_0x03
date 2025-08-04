#!/usr/bin/env python
"""
Live demo script that processes email tasks in real-time.
"""
import os
import sys
import django
import subprocess
import time
import signal
from threading import Thread

# Setup Django environment
sys.path.append("/home/meyvn/Desktop/ProDev-Backend/alx_travel_app_0x03/alx_travel_app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_travel_app.settings")
django.setup()

from listings.tasks import send_booking_confirmation_email
from listings.models import Booking


def run_celery_worker():
    """Run Celery worker in background"""
    try:
        os.chdir(
            "/home/meyvn/Desktop/ProDev-Backend/alx_travel_app_0x03/alx_travel_app"
        )
        process = subprocess.Popen(
            ["celery", "-A", "alx_travel_app", "worker", "--loglevel=info"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        print("🔄 Celery worker started...")

        # Print output in real-time
        for line in iter(process.stdout.readline, ""):
            print(line, end="")
            if "ready." in line:
                print("✅ Worker is ready!")
                break

        return process
    except Exception as e:
        print(f"❌ Error starting worker: {e}")
        return None


def main():
    print("🚀 Live Celery Email Demo")
    print("=" * 40)

    # Start worker
    worker_process = run_celery_worker()

    if not worker_process:
        print("❌ Failed to start worker")
        return

    try:
        # Wait a moment for worker to fully start
        time.sleep(3)

        # Get an existing booking or create one
        booking = Booking.objects.first()
        if not booking:
            print("❌ No bookings found. Run demo_celery_workflow.py first.")
            return

        print(f"\n📧 Triggering email for booking #{booking.id}")

        # Trigger the task
        result = send_booking_confirmation_email.delay(booking.id)
        print(f"✅ Task queued: {result.id}")

        # Wait for task to process
        print("\n⏳ Waiting for task to process...")
        time.sleep(5)

        # Check task result
        try:
            task_result = result.get(timeout=10)
            print(f"📬 Task completed: {task_result}")
        except Exception as e:
            print(f"⚠️  Task still processing or failed: {e}")

    finally:
        # Clean up
        print("\n🛑 Stopping worker...")
        worker_process.terminate()
        worker_process.wait()
        print("✅ Worker stopped")


if __name__ == "__main__":
    main()
