# Root-level settings.py
# This file serves as a reference/entry point to the main Django settings
# The actual Django settings are located at: alx_travel_app/alx_travel_app/settings.py

# Note: This is a reference file. To run Django commands, use:
# cd alx_travel_app && python manage.py [command]
# or use the provided script: ./django-manage.sh [command]

# Basic Django settings for reference
import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent

# SECURITY WARNING: This is a reference file only
SECRET_KEY = "reference-file-use-main-django-settings"
DEBUG = False
ALLOWED_HOSTS = []

# Database reference (actual config in alx_travel_app/alx_travel_app/settings.py)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "alx_travel_db",
        "USER": "travel_user",
        "PASSWORD": "travel_password",
        "HOST": "127.0.0.1",
        "PORT": "3308",
    }
}

# Main Django project location
DJANGO_PROJECT_PATH = BASE_DIR / "alx_travel_app"
DJANGO_SETTINGS_PATH = DJANGO_PROJECT_PATH / "alx_travel_app" / "settings.py"

print(f"Reference settings file. Main Django settings: {DJANGO_SETTINGS_PATH}")
