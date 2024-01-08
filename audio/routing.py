"""
routing.py file for audio app. Routing websocket connections to consumers.

Author(s): Benjamin Klieger
Version: 1.1.0
Date: 2024-01-07
"""

# Import Django Modules
from django.urls import re_path

# Import Consumers
from . import consumers

# Define websocket_urlpatterns
websocket_urlpatterns = [
    # re_path(r'listen/(?P<token>[\w-]+)/$', consumers.TranscriptConsumer.as_asgi()), Not being used currently, session transcript is made first then passed in the url now.
    re_path(r'listen/(?P<token>[\w-]+)/(?P<sessionid>[\w-]+)/$', consumers.TranscriptConsumerFollowup.as_asgi()),
]