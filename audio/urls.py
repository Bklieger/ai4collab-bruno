"""
urls.py file for audio app.

Author(s): Benjamin Klieger
Version: 1.0.1
Date: 2024-01-07
"""

# Import Django Modules
from django.urls import path

# Import Views
from .views import index, WebsocketTokenView, SessionTranscriptView

# Url Patterns
urlpatterns = [
    path('', index, name='index'), # Main interface
    path('api/token/', WebsocketTokenView.as_view(), name='token'), # Websocket token
    path('api/newsession/', SessionTranscriptView.as_view(), name='transcript'), # New session transcript
]