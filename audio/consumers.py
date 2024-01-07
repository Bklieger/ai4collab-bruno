"""
consumers.py file for audio app. Define consumers for ai4collab project to enable 
live transcription.

Author(s): Benjamin Klieger
Version: 1.0.1
Date: 2024-01-06
"""

#------- [Import Libraries] -------#

# Django and channels
from django.apps import apps
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

# Other libraries
from deepgram import Deepgram
from typing import Dict
from asgiref.sync import sync_to_async
import json
import os

# Utils 
from .utils import empty_string_if_none

# Import settings, warning: contains sensitive variables
from django.conf import settings


#------- [Environment Variables] -------#
DEEPGRAM_API_KEY = settings.DEEPGRAM_API_KEY


#------- [Define Consumers Below] -------#

# Consumer for live transcription
class TranscriptConsumer(AsyncWebsocketConsumer):
    dg_client = Deepgram(DEEPGRAM_API_KEY)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer = []
        """
        BUFFER_SIZE: 10 to start so the consumer does not have constant saving 
        which would be computationally expensive in DB writes. Has flush signal 
        function in case LLM response is requested or page is closed.
        """
        self.BUFFER_SIZE = 10
        self.session_id_token = None
        self.token_obj = None
        self.current_speaker = None

    @database_sync_to_async
    def save_transcripts(self):
        """
        Save the transcripts in the buffer to the database. 
        In other words, save then flush the buffer.
        
        Creates a new session if none is passed into the url.
        """

        SessionTranscript = apps.get_model('audio', 'SessionTranscript')

        # Define the total new content of the transcript from the buffer
        total_content = ""

        # Loop through the buffer and add to the total content
        for transcript in self.buffer:
            total_content += transcript
        
        # If the session id token is None, create a new session
        if self.session_id_token==None:
            #create new session
            self.session_id_token = SessionTranscript.objects.create(transcript=total_content, user=self.token_obj.user).id_token
        
        # Otherwise, add to the existing session
        else:
            if SessionTranscript.objects.filter(id_token=self.session_id_token).exists():
                # Add to existing session
                full_transcript = SessionTranscript.objects.get(id_token=self.session_id_token).transcript + total_content
                SessionTranscript.objects.filter(id_token=self.session_id_token).update(transcript=full_transcript)
            else:
                raise Exception(f'Could not find sessionid {sessionid} in database.')

        # Empty the buffer
        self.buffer = []


    # Get the transcript from the socket
    async def get_transcript(self, data: Dict) -> None:
        if 'channel' in data:
            #loop through words
            transcript = ""
            print(data['channel']['alternatives'][0]['words']) # Debugging

            # Add the new words to the transcript
            for word in data['channel']['alternatives'][0]['words']:
                if word['speaker'] != self.current_speaker:
                    if self.current_speaker == None:
                        transcript += f"Speaker {word['speaker']}: \n"
                    else:
                        transcript += f"\n\nSpeaker {word['speaker']}: \n"
                    
                    self.current_speaker = word['speaker']
                    
                    transcript += word['punctuated_word'] + " "
                else:
                    transcript += word['punctuated_word'] + " "
      
            # Add the transcript to the buffer if it is not empty
            if transcript != "" and transcript != None:
                self.buffer.append(transcript)

            # Save the transcripts if the buffer is full, then empty the buffer
            if len(self.buffer) >= self.BUFFER_SIZE:
                await self.save_transcripts()

            await self.send(transcript)


    # Connect to the Deepgram socket
    async def connect_to_deepgram(self):
       try:
           self.socket = await self.dg_client.transcription.live({'punctuate': True, 'interim_results': False, "diarize": True, 'tier':"nova",'model': 'general'})
           self.socket.registerHandler(self.socket.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))
           self.socket.registerHandler(self.socket.event.TRANSCRIPT_RECEIVED, self.get_transcript)

       except Exception as e:
           raise Exception(f'Could not open socket: {e}')


    # Connect to the websocket
    async def connect(self):
        WebsocketToken = apps.get_model('audio', 'WebsocketToken')
        token = self.scope['url_route']['kwargs']['token']
        self.token_obj = await sync_to_async(WebsocketToken.objects.get)(token=token)

        # Get the token
        try:
            self.token_obj = await sync_to_async(WebsocketToken.objects.get)(token=token)
        except:
            await self.close()
            return

        self.room_name = "basic_audio_connection"
        self.room_group_name = f'transcript_{self.room_name}'

        await self.connect_to_deepgram()
        await self.accept()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
    
    # Disconnect from the websocket
    async def disconnect(self, close_code):
       await self.channel_layer.group_discard(
           self.room_group_name,
           self.channel_name
       )


    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data: # If audio, send to deepgram socket
            self.socket.send(bytes_data)
        elif text_data: # If in text, execute command
            data = json.loads(text_data)

            # Flush buffer command
            if data.get('command') == 'flush_buffer':
                await self.save_transcripts()
                pass
            
            # Check for the keep_alive command from the frontend
            elif data.get('command') == 'keep_alive':
                print("Sending keep alive.")
                keep_alive_message = {'type': 'KeepAlive'}
                if self.socket:  # Check if socket is initialized
                    self.socket.send(json.dumps(keep_alive_message)) # Sends keep alive to deepgram socket


# Consumer for followup transcription, extending the TranscriptConsumer
class TranscriptConsumerFollowup(TranscriptConsumer):

    @database_sync_to_async
    def save_transcripts(self):
        """
        Save the transcripts in the buffer to the database. 
        In other words, save then flush the buffer.

        This function is different from the parent class because 
        it will not create a new session, as it assumes that the
        session already exists.
        """

        SessionTranscript = apps.get_model('audio', 'SessionTranscript')

        # Define the total new content of the transcript from the buffer
        total_content = ""
        for transcript in self.buffer:
            total_content += transcript

        # Get the session id token from the url
        sessionid = self.scope['url_route']['kwargs']['sessionid']
        
        # Add to the existing session
        if SessionTranscript.objects.filter(id_token=sessionid).exists():
            full_transcript = empty_string_if_none(SessionTranscript.objects.get(id_token=sessionid).transcript) + total_content
            SessionTranscript.objects.filter(id_token=sessionid).update(transcript=full_transcript)
        else:
            raise Exception(f'Could not find sessionid {sessionid} in database.')

        # Empty the buffer
        self.buffer = []

