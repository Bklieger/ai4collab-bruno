from django.urls import path

from .views import index, WebsocketTokenView, SessionTranscriptView

urlpatterns = [
    path('', index, name='index'),
    path('api/token/', WebsocketTokenView.as_view(), name='token'),
    path('api/newsession/', SessionTranscriptView.as_view(), name='transcript'),
]