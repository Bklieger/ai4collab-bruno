from django.contrib import admin
from .models import WebsocketToken, SessionTranscript

# Register your models here.
admin.site.register(WebsocketToken)
admin.site.register(SessionTranscript)