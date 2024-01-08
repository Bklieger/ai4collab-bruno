"""
models.py file for audio app. Define websocket token and session transcript models.

Author(s): Benjamin Klieger
Version: 1.0.1
Date: 2024-01-07
"""

#------- [Import Libraries] -------#

# Import Django Modules
from django.db import models
from accounts.models import CustomUser
import uuid


#------- [Models] -------#

# Websocket Token (Warning, this acts as auth for user with limited permissions)
class WebsocketToken(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE) # Token has a one to one relationship with CustomUser

    # Define custom string representation of WebsocketToken
    def __str__(self):
        return str(self.user) + " - " + str(self.token)

# Session Transcript
class SessionTranscript(models.Model):
    id_token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True) # Unique ID for each session
    transcript = models.TextField(null=True, blank=True) # Transcript of session
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) # User who generated the session
    session_title = models.CharField(max_length=255, null=True, blank=True) # Title of session (Future feature)

    # Define custom string representation of SessionTranscript
    def __str__(self):
        if self.session_title is None:
            return str(self.user) + " - " + str(self.id_token)
        else:
            return str(self.session_title) + " - " + str(self.user) + " - " + str(self.id_token)