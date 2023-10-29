# Ai4collab-Bruno

## What is Bruno?

Bruno is a speech-to-text-to-AI tool designed to facilitate collaborative learning in groupwork. The prototype application listens to human speech, provides a written transcript that identifies individual speakers, and passes the transcript and a chosen prompt to a LLM.

## How does Bruno work?

The backend serves HTML frontend. After the user logs in with Google, they have access to live transcription through audio data passed through the backend to Deepgram (transcription API) and relayed back to the frontend. This transcript is also stored in the database, allowing the user to ask Bruno (GPT with custom prompts and transcript) questions about the conversation.

## Description of Stack

The frontend is built with html and tailwindcss. The backend is built with the django rest framework, a decision made due to Django's robust feature set, out of the box admin and security capabilities, and compatability with the existing project code written in python. The project also leverages Docker to normalize runtime environments and increase the ease of collaboration.

## Release History

v1.0.0 - October 26th, 2023. First open-source stable version.

## License

GNU General Public License v3.0 or later

Contributors are able to contribute to the original codebase or create a forked open-source version. We request that you include [Principles.md](Principles.md) in any derivation of the codebase.

See [COPYING](COPYING) to view the full text.

---

# Instructions to Run

## Prepare Environment Variables

### Required Variables

Before you can deploy the application, you must first set your environment variables. This includes Google Oauth, deepgram, and OpenAI API keys.

### Local Deployment

For deploying the application locally, the following environment variables are required:


------- [local.env] --------

DEPLOYMENT=local

DJANGO_SETTINGS_MODULE=ai4collab.settings

DEEPGRAM_API_KEY=<add here>

MIDDLESIGHT_API_KEY=<add here> or OPENAI_API_KEY=<add here>

GOOGLE_CLIENT_ID=<add here>

GOOGLE_SECRET_KEY=<add here>

### Deployment Deployment

For deploying the application to a development environment, the following environment variables are required:


------- [development.env] --------

DEPLOYMENT=development  
DJANGO_SETTINGS_MODULE=ai4collab.settings  
SECRET_KEY=\<add here\>  
PSQL_DATABASE_URL=\<add here\>  
ALLOWED_HOSTS=\<add here\>  
DEEPGRAM_API_KEY=\<add here\>  
MIDDLESIGHT_API_KEY=\<add here\> or OPENAI_API_KEY=\<add here\>  
GOOGLE_CLIENT_ID=\<add here\>  
GOOGLE_SECRET_KEY=\<add here\>  


### Production Deployment

Finally, deploying the application to a production environment reqires the following environment variables:


------- [production.env] --------

DEPLOYMENT=production  
DJANGO_SETTINGS_MODULE=ai4collab.settings  
SECRET_KEY=\<add here\>  
PSQL_DATABASE_URL=\<add here\>  
ALLOWED_HOSTS=\<add here\>  
DEEPGRAM_API_KEY=\<add here\>  
MIDDLESIGHT_API_KEY=\<add here\> or OPENAI_API_KEY=\<add here\>  
GOOGLE_CLIENT_ID=\<add here\>  
GOOGLE_SECRET_KEY=\<add here\>  


### Descriptions of Variables

After selecting your deployment environment, the list of environment variables functions as a to-do list for setting up the project. Below are instructions for each variable.


#### DEPLOYMENT

The DEPLOYMENT variable is required for all deployments and is self explanatory; It can be set to local, development, or production.

#### DJANGO_SETTINGS_MODULE

The DJANGO_SETTINGS_MODULE variable is required for all deployments and does not need to be customized. It should be set to ai4collab.settings.

#### SECRET_KEY

The SECRET_KEY variable is required only for development and production deployments, as a hard-coded insecure key is used for local. The secret key is a requirement of Django applications and used for security. The key is typically 50 characters long, with a diverse set of letters, digits, and special characters. There are several generators that can be found online, or you can generate one by running the following command:


~~~
python -c 'import secrets; print(secrets.token_urlsafe(38))'
~~~

#### PSQL_DATABASE_URL

The PSQL_DATABASE_URL variable is required only for development and production deployments, as local deployment uses an SQLite database. PSQL_DATABASE_URL should include a PostgreSQL database with the username, password, host, port, and database name in the URL.

#### ALLOWED_HOSTS

The ALLOWED_HOSTS variable is a comma-seperated list of strings representing the allowed hosts for the Django app. This is required only for development and production deployments, as allowed hosts is set to "*" in local. An example for development is the following: ALLOWED_HOSTS=localhost,127.0.0.1,exampledev.railway.app

#### DEEPGRAM_API_KEY

The DEEPGRAM_API_KEY variable is required for all deployments. It can be obtained by creating a free account on deepgram.com, which will issue your account free credits to start.

#### MIDDLESIGHT_API_KEY

The MIDDLESIGHT_API_KEY variable is used for a custom configuration of Bruno. Specifically, the live application uses Middlesight to enable error tracking and rate limits. However, an easier implementation is to use the OpenAI API directly. Therefore, MIDDLESIGHT_API_KEY *should be ignored* and replaced with OPENAI_API_KEY.

#### OPENAI_API_KEY

The OPENAI_API_KEY variable is required for all deployments. It is the OpenAI API key used for powering Bruno. This is the only third-party API key for Bruno which may need payment information to activate.

#### GOOGLE_CLIENT_ID and GOOGLE_SECRET_KEY

The GOOGLE_CLIENT_ID and GOOGLE_SECRET_KEY are required for all deployments. In order to configure Google Oauth, you may consult the following link: https://support.google.com/googleapi/answer/6158849?hl=en


#### Next Steps

Once you have set all the variables in a file named {deployment}.env (e.g. local.env, development.env, production.env), you can move to the next step. Using docker is recommended, but instructions for deployment without docker are included.


## Run With Docker

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


## Run Without Docker

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

