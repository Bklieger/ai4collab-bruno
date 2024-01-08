"""
admin.py file for audio app.

Author(s): Benjamin Klieger
Version: 1.0.1
Date: 2024-01-07
"""

# Import Django Modules
from django.contrib import admin
from .models import WebsocketToken, SessionTranscript

# Register WebsocketToken and SessionTranscript models to Admin
admin.site.register(WebsocketToken)
admin.site.register(SessionTranscript)