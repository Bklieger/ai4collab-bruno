"""
Asgi.py:

ASGI config for ai4collab project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/

Author(s): Benjamin Klieger
Version: 1.1.0
Date: 2024-01-11
"""

# Import OS for environment variables
import os

# Import required channels and django libraries
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import audio.routing

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai4collab.settings")


application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            audio.routing.websocket_urlpatterns
        )
    ),
})