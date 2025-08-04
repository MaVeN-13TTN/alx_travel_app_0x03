# Root-level urls.py
# This file serves as a reference/entry point to the main Django URLs
# The actual Django URLs are located at: alx_travel_app/alx_travel_app/urls.py

# Note: This is a reference file. To run Django commands, use:
# cd alx_travel_app && python manage.py [command]
# or use the provided script: ./django-manage.sh [command]

from django.contrib import admin
from django.urls import path, include
from pathlib import Path

# Main Django project location
BASE_DIR = Path(__file__).resolve().parent
DJANGO_PROJECT_PATH = BASE_DIR / "alx_travel_app"
DJANGO_URLS_PATH = DJANGO_PROJECT_PATH / "alx_travel_app" / "urls.py"

# Reference URL patterns (actual patterns in main Django project)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("listings.urls")),
    # Add other URL patterns as needed
]

print(f"Reference URLs file. Main Django URLs: {DJANGO_URLS_PATH}")
