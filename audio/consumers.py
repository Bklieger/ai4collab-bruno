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

class TranscriptConsumer(AsyncWebsocketConsumer):
    dg_client = Deepgram(DEEPGRAM_API_KEY)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer = []
        self.BUFFER_SIZE = 10  # 10 to start so does not have constant saving which would be expensive. Has flush signal in case LLM response requested or closing page.
        self.session_id_token = None
        self.token_obj = None
        self.current_speaker = None

    @database_sync_to_async
    def save_transcripts(self):
        SessionTranscript = apps.get_model('audio', 'SessionTranscript')
        total_content = ""
        for transcript in self.buffer:
            total_content += transcript
        if self.session_id_token==None:
            #create new session
            self.session_id_token = SessionTranscript.objects.create(transcript=total_content, user=self.token_obj.user).id_token
        else: #TODO: make more efficient
            if SessionTranscript.objects.filter(id_token=self.session_id_token).exists():
                full_transcript = SessionTranscript.objects.get(id_token=self.session_id_token).transcript + total_content
                SessionTranscript.objects.filter(id_token=self.session_id_token).update(transcript=full_transcript)
            else:
                raise Exception(f'Could not find sessionid {sessionid} in database.')

        self.buffer = []

    async def get_transcript(self, data: Dict) -> None:
        if 'channel' in data:
            #loop through words
            transcript = ""
            print(data['channel']['alternatives'][0]['words'])
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
      
            if transcript != "" and transcript != None:

             self.buffer.append(transcript)

             if len(self.buffer) >= self.BUFFER_SIZE:
                 await self.save_transcripts()

             await self.send(transcript)


    async def connect_to_deepgram(self):
       try:
           self.socket = await self.dg_client.transcription.live({'punctuate': True, 'interim_results': False, "diarize": True, 'tier':"nova",'model': 'general'})
           self.socket.registerHandler(self.socket.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))
           self.socket.registerHandler(self.socket.event.TRANSCRIPT_RECEIVED, self.get_transcript)

       except Exception as e:
           raise Exception(f'Could not open socket: {e}')

    async def connect(self):
        WebsocketToken = apps.get_model('audio', 'WebsocketToken')
        token = self.scope['url_route']['kwargs']['token']
        self.token_obj = await sync_to_async(WebsocketToken.objects.get)(token=token)

        # Get the token
        try:
            self.token_obj = await sync_to_async(WebsocketToken.objects.get)(token=token)
        except: #TODO: make more specific
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
        
        
    async def disconnect(self, close_code):
       await self.channel_layer.group_discard(
           self.room_group_name,
           self.channel_name
       )

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            self.socket.send(bytes_data)
        elif text_data:
            data = json.loads(text_data)
            if data.get('command') == 'flush_buffer':
                await self.save_transcripts()
                pass
                # Check for the keep_alive command from the frontend
            elif data.get('command') == 'keep_alive':
                print("Sending keep alive.")
                keep_alive_message = {'type': 'KeepAlive'}
                if self.socket:  # Check if socket is initialized
                    self.socket.send(json.dumps(keep_alive_message)) # Sends keep alive to deepgram socket

class TranscriptConsumerFollowup(TranscriptConsumer):

    @database_sync_to_async
    def save_transcripts(self):
        SessionTranscript = apps.get_model('audio', 'SessionTranscript')


        total_content = ""
        for transcript in self.buffer:
            total_content += transcript

        sessionid = self.scope['url_route']['kwargs']['sessionid']
        
        if SessionTranscript.objects.filter(id_token=sessionid).exists():
            full_transcript = empty_string_if_none(SessionTranscript.objects.get(id_token=sessionid).transcript) + total_content
            SessionTranscript.objects.filter(id_token=sessionid).update(transcript=full_transcript)
        else:
            raise Exception(f'Could not find sessionid {sessionid} in database.')

        self.buffer = []