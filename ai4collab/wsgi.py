"""
wsgi.py file for ai4collab app.

WSGI config for ai4collab project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/

Author(s): Benjamin Klieger
Version: 1.0.0
Date: 2023-10-26
"""

# Import OS for environment variables
import os

# Import Django libraries
from django.core.wsgi import get_wsgi_application

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4collab.settings')

application = get_wsgi_application()