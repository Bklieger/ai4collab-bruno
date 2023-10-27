# Audio App

## Details
The audio app defines the WebsocketToken and SessionTranscript in models.py. The former is an auth token for each individual user that is used when connecting to the websocket. The later is the transcript for each session. Consumers.py and routing.py define the websocket for live transcription with deepgram.

## How is the transcript stored?
As the audio data is transcribed through the websocket, it is returned to the frontend live. In addition, the transcript is stored in the SessionTranscript object in the backend database. When Bruno is prompted, the backend retrieves the transcript from the SessionTranscript object, rather than the transcript being passed in through the frontend, since the backend already has access to the transcript through the database. 

In addition, before Bruno is prompted, the websocket sends a signal for the backend to store and flush the buffer of the transcription. This is because the websocket keeps a buffer of the transcription returned by deepgram and intermittently stores the results in the database SessionTranscript object. This is a more efficient system as it minimizes unnecessary modifications of the SessionTranscript object in the database.

## Audio to Text Details

The application currently utilizes deepgram's live transcription and diarization. When the recording is paused, the websocket with the backend as a proxy to deepgram is still open, but no audio data is sent. The socket is kept alive using a keepAlive message sent to the backend then to Deepgram.
