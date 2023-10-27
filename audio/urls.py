"""
urls.py file for audio app.

Author(s): Benjamin Klieger
Version: 1.0.0
Date: 2023-10-26
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