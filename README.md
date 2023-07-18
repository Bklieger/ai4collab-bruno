# Ai4collab

## Ai4collab-backend Description of Features

The ai4collab backend receives audio file input from a time interval on the frontend to create a transcript for the conversation, and allow the user to query a LLM with the transcript and a customizable prompt. 

## Ai4collab-backend Description of Stack

The ai4collab backend is built with the django rest framework, a decision made due to Django's robust feature set, out of the box admin and security capabilities, and compatability with the existing project code written in python.

The project also leverages Docker to normalize runtime environments and increase the ease of collaboration.

## Ai4collab-backend Release History

In development

## Ai4collab-backend Instructions to Run

## Instructions with Docker

### To build the docker image
~~~
docker build -t ai4collab:latest .
~~~

### Run docker image in same directory as env file
~~~
docker run --env-file {DEPLOYMENT}.env -p 8000:8000 ai4collab:latest
~~~
DEPLOYMENT = local, development, or production. Run with -d for detached.


# Instructions without Docker

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

### Set environmental variables
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

### Run server without Gunicorn
~~~
python manage.py runserver
~~~

### Alternative: Run server with Gunicorn
~~~
gunicorn --bind 0.0.0.0:8000 --workers 4 ai4collab.wsgi
~~~

The application is now up and running!