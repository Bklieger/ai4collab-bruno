"""
urls.py file for ai4collab app.

Author(s): Benjamin Klieger
Version: 1.1.0
Date: 2024-01-11
"""

# Import Django Modules
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

# Import Views
from .views import deployment_status

# Url Patterns
urlpatterns = [
    path('', include('audio.urls')), # Include audio app urls
    path('', include('llm.urls')), # Include llm app urls
    path('accounts/', include('accounts.urls')), # Include accounts app urls
    path('admin/', admin.site.urls), # Include admin urls
    path('deployment/', deployment_status, name='deployment'), # Deployment status page
    path('allauth/', include('allauth.urls')), # Include allauth urls
]
