#!/bin/bash

# Script to test Celery with RabbitMQ setup
echo "Testing Celery and RabbitMQ setup for ALX Travel App..."

# Navigate to project directory
cd /home/meyvn/Desktop/ProDev-Backend/alx_travel_app_0x03

# Activate virtual environment
source venv/bin/activate

echo "1. Checking if RabbitMQ is running..."
if sudo systemctl is-active --quiet rabbitmq-server; then
    echo "✓ RabbitMQ is running"
else
    echo "✗ RabbitMQ is not running. Starting it..."
    sudo systemctl start rabbitmq-server
fi

echo ""
echo "2. Testing Celery connection..."
echo "Starting Celery worker in background (this will run for 10 seconds)..."

# Start Celery worker in background for testing
timeout 10s celery -A alx_travel_app worker --loglevel=info &
WORKER_PID=$!

sleep 2

echo ""
echo "3. Testing a simple Celery task..."
# Create a simple test script
cat > test_celery_task.py << 'EOF'
import os
import django
import sys

# Setup Django environment
sys.path.append('/home/meyvn/Desktop/ProDev-Backend/alx_travel_app_0x03/alx_travel_app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')
django.setup()

from listings.tasks import send_booking_confirmation_email

# Try to call the task (this will fail but show if Celery is working)
try:
    result = send_booking_confirmation_email.delay(1)
    print(f"✓ Task queued successfully with ID: {result.id}")
    print("✓ Celery and RabbitMQ are working correctly!")
except Exception as e:
    print(f"✗ Error queuing task: {e}")
EOF

python test_celery_task.py

# Clean up
rm test_celery_task.py

echo ""
echo "4. Stopping test worker..."
if ps -p $WORKER_PID > /dev/null 2>&1; then
    kill $WORKER_PID
fi

echo ""
echo "Setup verification complete!"
echo ""
echo "To start Celery worker for production:"
echo "celery -A alx_travel_app worker --loglevel=info"
echo ""
echo "To monitor tasks:"
echo "celery -A alx_travel_app flower  # Install flower first: pip install flower"
