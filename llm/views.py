"""
views.py file for llm app.

Author(s): Benjamin Klieger
Version: 1.1.0
Date: 2024-01-07
"""

#------- [Import Libraries] -------#

# Django imports
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from audio.models import SessionTranscript

# Import util function of LLM API
from .utils import get_llm_feedback


#------- [Define Views] -------#

@method_decorator(login_required, name='dispatch')
class LlmView(APIView):
    def get(self, request):
        try:
            #get SessionTranscriptID from request
            session_transcript_id = request.GET.get('session_transcript_id')
            if session_transcript_id is None: # if session_transcript_id is not provided
                return Response({"error": "session_transcript_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            prompt_for_llm = request.GET.get('prompt_for_llm')
            if prompt_for_llm is None or prompt_for_llm=="": # if prompt_for_llm is not provided or is empty
                return Response({"error": "prompt_for_llm is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            #get SessionTranscript object
            object_for_response = SessionTranscript.objects.get(user=request.user, id_token=session_transcript_id)

            # double check that session transcript is owned by user
            if object_for_response.user != request.user:
                return Response({"error": "session_transcript_id is invalid"}, status=status.HTTP_400_BAD_REQUEST)

            # get transcript from session transcript
            transcript_from_session_transcript = object_for_response.transcript
            
            # return error if transcript is empty
            if transcript_from_session_transcript==None:
                return Response({"error": "transcript is empty"}, status=status.HTTP_400_BAD_REQUEST)

            # get response from LLM, formatting the instructions and transcript
            prompt_for_llm = "Transcript: \n\n"+transcript_from_session_transcript+"\n--------------\n\nInstructions: "+prompt_for_llm
            response_from_llm = get_llm_feedback(prompt_for_llm)
            
            # return response from LLM
            return Response({"prompt_for_llm":prompt_for_llm,"response_from_llm": response_from_llm})

        # if session_transcript_id is invalid
        except SessionTranscript.DoesNotExist:
            # return error
            return Response({"error": "session_transcript_id is invalid"}, status=status.HTTP_400_BAD_REQUEST)
    

@method_decorator(login_required, name='dispatch')
class LlmOnlyView(APIView):
    def get(self, request):
        #get SessionTranscriptID from request
        transcript = request.GET.get('transcript')
        if transcript is None: # if session_transcript_id is not provided
            return Response({"error": "transcript is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        prompt_for_llm = request.GET.get('prompt_for_llm')
        if prompt_for_llm is None or prompt_for_llm=="": # if prompt_for_llm is not provided or is empty
            return Response({"error": "prompt_for_llm is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # get response from LLM, formatting the instructions and transcript
        prompt_for_llm = "Transcript: \n\n"+transcript+"\n--------------\n\nInstructions: "+prompt_for_llm
        response_from_llm = get_llm_feedback(prompt_for_llm)
        
        # return response from LLM
        return Response({"prompt_for_llm":prompt_for_llm,"response_from_llm": response_from_llm})