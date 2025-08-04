"""
Celery tasks for the listings app.

This module contains background tasks for email notifications and other async operations.
"""

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Payment, Booking


@shared_task
def send_payment_confirmation_email(payment_id):
    """
    Send a payment confirmation email to the user.

    Args:
        payment_id: The ID of the payment to send confirmation for
    """
    try:
        payment = Payment.objects.get(id=payment_id)
        booking = payment.booking
        user = booking.user

        subject = "Payment Confirmation for your Booking"
        message = f"""
        Dear {user.first_name},

        This is a confirmation that your payment for the booking of "{booking.listing.title}" has been successfully processed.

        Booking Details:
        - Check-in: {booking.check_in_date}
        - Check-out: {booking.check_out_date}
        - Total Amount: {payment.amount} ETB
        - Transaction ID: {payment.transaction_id}

        Thank you for choosing Alx Travel.

        Best regards,
        The Alx Travel Team
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return f"Confirmation email sent to {user.email} for payment {payment_id}"
    except Payment.DoesNotExist:
        return f"Payment with id {payment_id} does not exist."
    except Exception as e:
        return f"Failed to send email for payment {payment_id}: {str(e)}"


@shared_task
def send_booking_confirmation_email(booking_id):
    """
    Send a booking confirmation email to the user when a new booking is created.

    Args:
        booking_id: The ID of the booking to send confirmation for
    """
    try:
        booking = Booking.objects.get(id=booking_id)
        user = booking.user

        subject = f"Booking Confirmation - {booking.listing.title}"
        message = f"""
        Dear {user.first_name} {user.last_name},
        
        Thank you for your booking! Your reservation has been successfully created.
        
        Booking Details:
        - Booking ID: #{booking.id}
        - Listing: {booking.listing.title}
        - Location: {booking.listing.location}
        - Check-in Date: {booking.check_in_date}
        - Check-out Date: {booking.check_out_date}
        - Number of Guests: {booking.num_guests}
        - Total Price: ETB {booking.total_price}
        - Status: {booking.get_status_display()}
        
        What's Next?
        - Your booking is currently {booking.status}
        - You will receive payment instructions shortly
        - Once payment is completed, your booking will be confirmed
        
        If you have any questions, please don't hesitate to contact us.
        
        Best regards,
        ALX Travel Team
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return f"Booking confirmation email sent to {user.email}"

    except Booking.DoesNotExist:
        return f"Booking with ID {booking_id} not found"
    except Exception as e:
        return f"Error sending booking confirmation email: {str(e)}"
