from django.db import models
from accounts.models import CustomUser
import uuid

# Websocket Token (Warning, this acts as limited Auth)
class WebsocketToken(models.Model):
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " - " + str(self.token)

# Session transcript
class SessionTranscript(models.Model):
    id_token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    transcript = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session_title = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.session_title is None:
            return str(self.user) + " - " + str(self.id_token)
        else:
            return str(self.session_title) + " - " + str(self.user) + " - " + str(self.id_token)