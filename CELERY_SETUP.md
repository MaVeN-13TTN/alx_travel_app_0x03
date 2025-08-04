# Celery with RabbitMQ Background Tasks Setup

This document explains how to configure and use Celery with RabbitMQ for background email notifications in the ALX Travel App.

## Overview

The application now uses Celery with RabbitMQ to handle background tasks, specifically:

- **Booking Confirmation Emails**: Sent automatically when a new booking is created
- **Payment Confirmation Emails**: Sent when a payment is successfully processed

## Architecture

```
Django App → Celery Tasks → RabbitMQ Broker → Celery Worker → Email Sending
```

## Setup Instructions

### 1. Install and Configure RabbitMQ

Run the provided setup script:

```bash
./setup_rabbitmq.sh
```

This will:

- Install RabbitMQ server
- Start the service
- Enable management plugin (optional web UI)

### 2. Configure Email Settings

Update your `.env` file with email credentials:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=ALX Travel <noreply@alxtravel.com>
```

**Note**: For Gmail, use an App Password instead of your regular password.

### 3. Start Celery Worker

In a separate terminal, start the Celery worker:

```bash
cd /home/meyvn/Desktop/ProDev-Backend/alx_travel_app_0x03
source venv/bin/activate
celery -A alx_travel_app worker --loglevel=info
```

### 4. Test the Setup

Run the test script:

```bash
./test_celery_setup.sh
```

## Email Tasks

### 1. Booking Confirmation Email (`send_booking_confirmation_email`)

**Trigger**: Automatically sent when a new booking is created via the BookingViewSet
**Content**: Booking details, what's next information
**Recipient**: The user who made the booking

### 2. Payment Confirmation Email (`send_payment_confirmation_email`)

**Trigger**: Sent after successful payment verification
**Content**: Payment details, booking confirmation
**Recipient**: The user who made the payment

## Implementation Details

### Celery Configuration (settings.py)

```python
CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
CELERY_RESULT_BACKEND = "rpc://"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
```

### Task Definition (listings/tasks.py)

```python
@shared_task
def send_booking_confirmation_email(booking_id):
    # Task implementation
```

### Task Triggering (listings/views.py)

```python
def perform_create(self, serializer):
    booking = serializer.save(user=self.request.user)
    send_booking_confirmation_email.delay(booking.id)
```

## Development vs Production

### Development

- Use console email backend for testing:
  ```python
  EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
  ```
- Single worker is sufficient

### Production

- Use SMTP backend with real email service
- Multiple workers for scalability:
  ```bash
  celery -A alx_travel_app worker --loglevel=info --concurrency=4
  ```
- Consider using supervisord or systemd for process management

## Monitoring

### Celery Flower (Optional)

Install and run Flower for task monitoring:

```bash
pip install flower
celery -A alx_travel_app flower
```

Access at: http://localhost:5555

### RabbitMQ Management UI

Access at: http://localhost:15672 (guest/guest)

## File Structure

```
alx_travel_app/
├── alx_travel_app/
│   ├── celery.py          # Celery app configuration
│   └── settings.py        # Celery settings
├── listings/
│   ├── tasks.py           # Email tasks
│   └── views.py           # Task triggering
├── setup_rabbitmq.sh      # RabbitMQ setup script
├── test_celery_setup.sh   # Test script
└── .env                   # Email configuration
```

## Troubleshooting

### Common Issues

1. **RabbitMQ not running**

   ```bash
   sudo systemctl start rabbitmq-server
   ```

2. **Email not sending**

   - Check email credentials in .env
   - Verify EMAIL_BACKEND setting
   - Check Celery worker logs

3. **Tasks not being processed**
   - Ensure Celery worker is running
   - Check RabbitMQ status
   - Verify Celery configuration

### Logs

- Celery worker logs: Shows task execution
- Django logs: Shows task queuing
- RabbitMQ logs: Shows message broker status

## API Workflow

### Booking Creation Flow

1. User creates booking via `/api/bookings/`
2. BookingViewSet.perform_create() is called
3. Booking is saved to database
4. `send_booking_confirmation_email.delay(booking.id)` queues task
5. Celery worker processes task and sends email

### Payment Confirmation Flow

1. Payment is verified via `/api/payments/verify/`
2. Payment and booking status updated
3. `send_payment_confirmation_email.delay(payment.id)` queues task
4. Celery worker processes task and sends email

## Security Notes

- Email credentials stored in environment variables
- RabbitMQ uses default guest/guest for development
- For production, create dedicated RabbitMQ user
- Use SSL/TLS for email connections

## Performance Considerations

- Tasks are asynchronous - don't block API responses
- Email sending happens in background
- RabbitMQ provides reliable message queuing
- Workers can be scaled horizontally
