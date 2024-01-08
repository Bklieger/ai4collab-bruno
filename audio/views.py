"""
utils.py file for audio app.

Author(s): Benjamin Klieger
Version: 1.0.1
Date: 2024-01-07
"""

#------- [Import Libraries] -------#

# Import Django Modules
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Import Models of WebsocketToken and SessionTranscript
from .models import WebsocketToken, SessionTranscript


# Import settings, warning: contains sensitive variables
from django.conf import settings

#------- [Environment Variables] -------#
# Define DEPLOYMENT variable
DEPLOYMENT = settings.DEPLOYMENT

# Login protected interface screen
@login_required
def index(request):
    # Determine URL to use depending on deployment
    if DEPLOYMENT != "production":
        url_to_use = "localhost:8000" # If hosting on different port, update this variable
        url_to_use = "ws://"+url_to_use
    else:
        url_to_use = "ai4collab.up.railway.app" # If hosting on different url, update this variable
        url_to_use = "wss://"+url_to_use
    return render(request, 'audio/index.html', {'url_to_use': url_to_use})


@method_decorator(login_required, name='dispatch')
class WebsocketTokenView(APIView):
    def get(self, request):
        try:
            object_for_token = WebsocketToken.objects.get(user=request.user)
            return Response({"token": object_for_token.token})
        except WebsocketToken.DoesNotExist:
            #make a new token
            object_for_token = WebsocketToken.objects.create(user=request.user)
            return Response({"token": object_for_token.token})


@method_decorator(login_required, name='dispatch')
class SessionTranscriptView(APIView):
    def get(self, request):
        object_for_id_token = SessionTranscript.objects.create(user=request.user)
        return Response({"session_id_token": object_for_id_token.id_token})