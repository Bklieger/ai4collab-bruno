from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'listen/(?P<token>[\w-]+)/$', consumers.TranscriptConsumer.as_asgi()), Not being used currently, session transcript is made first then passed in now. Delete later.
    re_path(r'listen/(?P<token>[\w-]+)/(?P<sessionid>[\w-]+)/$', consumers.TranscriptConsumerFollowup.as_asgi()),
]