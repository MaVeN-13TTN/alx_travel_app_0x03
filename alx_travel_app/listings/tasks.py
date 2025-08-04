from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Payment


@shared_task
def send_payment_confirmation_email(payment_id):
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
