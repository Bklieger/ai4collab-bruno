from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import WebsocketToken, SessionTranscript


# For testing
@login_required
def index(request):
    return render(request, 'audio/index.html')


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