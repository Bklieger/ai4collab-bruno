# Ai4collab-Bruno

## What is Bruno?


## How does Bruno work?

The backend serves HTML frontend. After the user logs in with Google, they have access to live transcription through audio data passed through the backend to Deepgram (transcription API) and relayed back to the frontend. This transcript is also stored in the database, allowing the user to ask Bruno (GPT with custom prompts and transcript) questions about the conversation.

## Description of Stack

The frontend is built with html and tailwindcss. The backend is built with the django rest framework, a decision made due to Django's robust feature set, out of the box admin and security capabilities, and compatability with the existing project code written in python. The project also leverages Docker to normalize runtime environments and increase the ease of collaboration.

## Release History

In development

---

# Instructions to Run

## With Docker

### To build the docker image
~~~
docker build -f Dockerfile.norail -t ai4collab:latest .
~~~

### Run docker image in same directory as env file
~~~
docker run --env-file {DEPLOYMENT}.env -p 8000:8000 ai4collab:latest
~~~
DEPLOYMENT = local, development, or production. Run with -d for detached.

The application is now up and running!


## Without Docker

### To create virtual env
~~~
python -m venv venv
~~~

### To activate virtual env
~~~
source venv/bin/activate
~~~

### To install libraries
~~~
pip install -r requirements.txt
~~~

### Set environment variables
~~~
touch {DEPLOYMENT}.env
~~~
DEPLOYMENT = local, development, or production

~~~
export $(cat {DEPLOYMENT}.env | xargs)
~~~

### Check status for production
~~~
python manage.py test
python manage.py check --deploy
~~~

### Initialize or update database
~~~
python manage.py makemigrations
python manage.py migrate
~~~

### Collect static files
~~~
python manage.py collectstatic
~~~

### Create superuser (optional)
~~~
python manage.py createsuperuser
~~~

### Run server with Uvicorn
~~~
uvicorn ai4collab.asgi:application
~~~

### Run server with Gunicorn running Uvicorn Workers
~~~
gunicorn --bind 0.0.0.0:8000 --workers 4 -k uvicorn.workers.UvicornWorker ai4collab.asgi:application
~~~

The application is now up and running!
