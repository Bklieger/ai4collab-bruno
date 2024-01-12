"""
urls.py file for audio app.

Author(s): Benjamin Klieger
Version: 1.1.0
Date: 2024-01-11
"""

# Import Django Modules
from django.urls import path

# Import Views
from .views import dashboard, customTranscriptDashboard, WebsocketTokenView, SessionTranscriptView

# Url Patterns
urlpatterns = [
    path('', dashboard, name='dashboard'), # Main interface
    path('upload', customTranscriptDashboard, name='dashboard'), # Alternative interface
    path('api/token/', WebsocketTokenView.as_view(), name='token'), # Websocket token
    path('api/newsession/', SessionTranscriptView.as_view(), name='transcript'), # New session transcript
]