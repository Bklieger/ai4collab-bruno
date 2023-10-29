"""
admin.py file for audio app.

Author(s): Benjamin Klieger
Version: 1.0.0
Date: 2023-10-26
"""

# Import Django Modules
from django.contrib import admin
from .models import WebsocketToken, SessionTranscript

# Register WebsocketToken and SessionTranscript models to Admin
admin.site.register(WebsocketToken)
admin.site.register(SessionTranscript)