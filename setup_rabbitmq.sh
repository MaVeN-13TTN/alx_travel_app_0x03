#!/bin/bash

# Script to set up RabbitMQ for Celery background tasks
echo "Setting up RabbitMQ for ALX Travel App..."

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install RabbitMQ server
echo "Installing RabbitMQ server..."
sudo apt install -y rabbitmq-server

# Start and enable RabbitMQ service
echo "Starting RabbitMQ service..."
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server

# Enable RabbitMQ management plugin (optional, for web UI)
echo "Enabling RabbitMQ management plugin..."
sudo rabbitmq-plugins enable rabbitmq_management

# Create a user for the application (optional, using guest for simplicity)
echo "RabbitMQ setup completed!"
echo ""
echo "RabbitMQ Status:"
sudo systemctl status rabbitmq-server --no-pager

echo ""
echo "RabbitMQ is now running and ready for Celery!"
echo "- Broker URL: amqp://guest:guest@localhost:5672//"
echo "- Management UI (if enabled): http://localhost:15672"
echo "- Default credentials: guest/guest"
echo ""
echo "To start Celery worker, run:"
echo "cd /home/meyvn/Desktop/ProDev-Backend/alx_travel_app_0x03"
echo "source venv/bin/activate"
echo "celery -A alx_travel_app worker --loglevel=info"
