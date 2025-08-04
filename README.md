# ALX Travel App - Backend

A Django REST API for a travel application with MySQL container setup and Chapa payment integration.

[![Django Version](https://img.shields.io/badge/Django-5.2.1-green.svg)](https:## 📁 Project Structure

````
ALX_TRAVEL_APP_0X03/
├── alx_travel_app/
│   ├── alx_travel_app/          # Django project settings
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── celery_app.py
│   │   ├── celery.py
│   │   ├── settings.py
│   │   ├── settings1.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── listings/                # Main application
│   │   ├── management/
│   │   │   ├── commands/
│   │   │   └── __init__.py
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── manage.py
├── venv/                        # Virtual environment
├── docker-compose.yml           # Docker configuration
├── requirements.txt             # Python dependencies
├── requirement.txt              # Alternative requirements file
├── .env                        # Environment variables
├── .env.example                # Environment template
├── settings.py                 # Root-level settings
├── urls.py                     # Root-level URLs
├── .gitignore
└── README.md
```ect.com/)
[![Python Version](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org/)
[![DRF Version](https://img.shields.io/badge/DRF-3.16.0-orange.svg)](https://www.django-rest-framework.org/)
[![Chapa](https://img.shields.io/badge/Payment-Chapa-purple)](https://chapa.co/)

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.12+
- Git

### 1. Clone and Setup

```bash
git clone <repository-url>
cd alx_travel_app_0x03
````

### 2. Environment Setup

Create your environment configuration:

```bash
cp .env.example .env
# Edit .env with your specific values if needed
```

### 3. Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 4. MySQL Container

Start the MySQL container:

```bash
docker compose up -d mysql
```

The MySQL container will be available on port **3308** (to avoid conflicts with local MySQL installations).

### 5. Database Setup

```bash
# Navigate to the Django project directory
cd alx_travel_app

# Activate virtual environment first
source ../venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py seed
```

### 6. Start Development Server

```bash
# From the alx_travel_app directory
cd alx_travel_app
source ../venv/bin/activate
python manage.py runserver
```

## 🔧 Quick Commands

For easier project management, use the provided scripts:

### Docker Management

```bash
# Container Management
./docker-manage.sh start     # Start MySQL container
./docker-manage.sh stop      # Stop MySQL container
./docker-manage.sh status    # Check container status
./docker-manage.sh shell     # Access MySQL shell
```

### Django Management

```bash
# Django Development (from project root)
./django-manage.sh server         # Start development server
./django-manage.sh migrate        # Run migrations
./django-manage.sh superuser      # Create superuser
./django-manage.sh test           # Run tests
./django-manage.sh check          # Check configuration

# Or manually (from alx_travel_app directory)
cd alx_travel_app
source ../venv/bin/activate
python manage.py runserver        # Start server
```

## 🐳 Docker Configuration

### MySQL Container Details

- **Image**: mysql:8.0
- **Container Name**: alx_travel_mysql
- **Port**: 3308 (host) → 3306 (container)
- **Database**: alx_travel_db
- **User**: travel_user
- **Password**: travel_password

### Useful Docker Commands

```bash
# Start MySQL container
docker compose up -d mysql

# Stop MySQL container
docker compose down

# View container logs
docker logs alx_travel_mysql

# Access MySQL shell
mysql -h 127.0.0.1 -P 3308 -u travel_user -ptravel_password alx_travel_db

# Reset database (removes all data!)
docker compose down -v
docker compose up -d mysql
python manage.py migrate
```

## 📊 Database Configuration

The application is configured to connect to the MySQL container with these settings:

```python
# .env file
DB_NAME=alx_travel_db
DB_USER=travel_user
DB_PASSWORD=travel_password
DB_HOST=127.0.0.1
DB_PORT=3308
```

## 🛠️ Development

### API Endpoints

- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/swagger/
- **API Root**: http://localhost:8000/api/

### Payment Integration

This project includes Chapa payment gateway integration for booking payments.

### Running Tests

```bash
# Navigate to Django project
cd alx_travel_app
source ../venv/bin/activate

# Run all tests
python manage.py test

# Run specific app tests
python manage.py test listings
```

### Management Commands

```bash
# Navigate to Django project
cd alx_travel_app
source ../venv/bin/activate

# Seed database with sample data
python manage.py seed

# Clear and reseed database
python manage.py seed --clear
```

## 🔧 Troubleshooting

### MySQL Connection Issues

1. Ensure the MySQL container is running:

   ```bash
   docker compose ps
   ```

2. Check container logs:

   ```bash
   docker logs alx_travel_mysql
   ```

3. Test direct connection:
   ```bash
   mysql -h 127.0.0.1 -P 3308 -u travel_user -ptravel_password -e "SELECT 'OK' as status;"
   ```

### Port Conflicts

If port 3308 is in use, modify `docker-compose.yml`:

```yaml
ports:
  - "3309:3306" # Change to available port
```

Then update `.env`:

```bash
DB_PORT=3309
```

## � Project Structure

```
alx_travel_app_0x03/
├── alx_travel_app/          # Django project settings
├── listings/                # Main application
├── venv/                    # Virtual environment
├── docker-compose.yml       # Docker configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── manage.py               # Django management script
```

## 🔐 Security Notes

- The `.env` file contains development credentials
- Change all passwords in production
- Never commit `.env` to version control
- The MySQL container uses development settings

## 📝 Environment Variables

| Variable               | Description       | Default                                       |
| ---------------------- | ----------------- | --------------------------------------------- |
| `SECRET_KEY`           | Django secret key | Development key                               |
| `DEBUG`                | Debug mode        | `True`                                        |
| `DB_NAME`              | Database name     | `alx_travel_db`                               |
| `DB_USER`              | Database user     | `travel_user`                                 |
| `DB_PASSWORD`          | Database password | `travel_password`                             |
| `DB_HOST`              | Database host     | `127.0.0.1`                                   |
| `DB_PORT`              | Database port     | `3308`                                        |
| `ALLOWED_HOSTS`        | Allowed hosts     | `localhost,127.0.0.1,0.0.0.0`                 |
| `CORS_ALLOWED_ORIGINS` | CORS origins      | `http://localhost:3000,http://127.0.0.1:3000` |
| `CHAPA_SECRET_KEY`     | Chapa payment key | Required for payments                         |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

This project is licensed under the terms specified in the LICENSE file.
