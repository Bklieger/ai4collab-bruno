"""
Django settings for ai4collab project.

Environment Variables:
    - GOOGLE_CLIENT_ID: A string representing the Google OAuth2 client ID.
        [Environment variable in: local, development, production]
    - GOOGLE_CLIENT_SECRET: A string representing the Google OAuth2 client secret.
        [Environment variable in: local, development, production]
    - DJANGO_SETTINGS_MODULE: Required for running, always ai4collab.settings
        [Environment variable in: local, development, production (all)]
    - DEPLOYMENT: A string representing the deployment environment.
        [Options: local, development, production]
    - SECRET_KEY: A secret key for the Django project.
        [Environment variable in: production]
    - DEBUG: A boolean value for whether or not to run in debug mode.
    - ALLOWED_HOSTS: A list of strings representing the allowed hosts.
        [Environment variable in: development, production]
    - PSQL_DATABASE_URL: A string representing the database URL.
        [Environment variable in: development, production]
    - DEEPGRAM_API_KEY: A string representing the Deepgram API key.
        [Environment variable in: local, development, production]
    - MIDDLESIGHT_API_KEY: A string representing the Middlesight API key.
        [Environment variable in: local, development, production]

Requirements for each deployment environment:
    Local: GOOGLE_CLIENT_ID, GOOGLE_SECRET_KEY, DJANGO_SETTINGS_MODULE, DEEPGRAM_API_KEY, MIDDLESIGHT_API_KEY required. DEPLOYMENT recommended.
    Development: GOOGLE_CLIENT_ID, GOOGLE_SECRET_KEY, DJANGO_SETTINGS_MODULE, DEPLOYMENT, SECRET_KEY, PSQL_DATABASE_URL, ALLOWED_HOSTS, DEEPGRAM_API_KEY, MIDDLESIGHT_API_KEY required.
    Production: GOOGLE_CLIENT_ID, GOOGLE_SECRET_KEY, DJANGO_SETTINGS_MODULE, DEPLOYMENT, SECRET_KEY, PSQL_DATABASE_URL, ALLOWED_HOSTS, DEEPGRAM_API_KEY, MIDDLESIGHT_API_KEY required.


------- [local.env] --------
DEPLOYMENT=local
DJANGO_SETTINGS_MODULE=ai4collab.settings
DEEPGRAM_API_KEY=<add here>
MIDDLESIGHT_API_KEY=<add here>
GOOGLE_CLIENT_ID=<add here>
GOOGLE_SECRET_KEY=<add here>

------- [development.env] --------
DEPLOYMENT=development
DJANGO_SETTINGS_MODULE=ai4collab.settings
SECRET_KEY=<add here>
PSQL_DATABASE_URL=<add here>
ALLOWED_HOSTS=<add here>
DEEPGRAM_API_KEY=<add here>
MIDDLESIGHT_API_KEY=<add here>
GOOGLE_CLIENT_ID=<add here>
GOOGLE_SECRET_KEY=<add here>

------- [production.env] --------
DEPLOYMENT=production
DJANGO_SETTINGS_MODULE=ai4collab.settings
SECRET_KEY=<add here>
PSQL_DATABASE_URL=<add here>
ALLOWED_HOSTS=<add here>
DEEPGRAM_API_KEY=<add here>
MIDDLESIGHT_API_KEY=<add here>
GOOGLE_CLIENT_ID=<add here>
GOOGLE_SECRET_KEY=<add here>

------- [instructions] -------
1. Create and fill env file
2. RUN export $(cat {deployment}.env | xargs)

"""


# ------------- [Import Libraries] -------------

# Import the pathlib, os, warnings, and inspect libraries.
from pathlib import Path
import os
import warnings
import inspect

# Import dj_database_url for database configuration.
import dj_database_url

# Import functions from the global_utils.py file.
from .global_utils import green_success, yellow_warning, red_critical


# ------------- [Important Variables] -------------

"""
The following variables are used in the deployment process to track outcomes and context.
"""

# For use in building the deployment transcript to inform user of deployment status.
running_deployment_transcript = ""
critical_warnings_exist = False

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------- [Environment Variables] -------------

"""
The following environment variables are used as API keys for 3rd party applications. 

Requirements:
    - DEEPGRAM_API_KEY: A string representing the Deepgram API key.
        [Environment variable in: local, development, production]
    - MIDDLESIGHT_API_KEY: A string representing the Middlesight API key.
        [Environment variable in: local, development, production]
"""

# Deepgram API key
DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY")

if DEEPGRAM_API_KEY==None:
    running_deployment_transcript+= red_critical(f'[Critical] DEEPGRAM_API_KEY environment variable not set. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
    critical_warnings_exist = True

elif len(DEEPGRAM_API_KEY)<3:
    running_deployment_transcript+= red_critical(f'[Critical] DEEPGRAM_API_KEY environment variable is invalid (<3 chars). (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
    critical_warnings_exist = True


# Middlesight API key
MIDDLESIGHT_API_KEY = os.environ.get("MIDDLESIGHT_API_KEY")

if MIDDLESIGHT_API_KEY==None:
    running_deployment_transcript+= red_critical(f'[Critical] MIDDLESIGHT_API_KEY environment variable not set. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
    critical_warnings_exist = True

elif len(MIDDLESIGHT_API_KEY)<3:
    running_deployment_transcript+= red_critical(f'[Critical] MIDDLESIGHT_API_KEY environment variable is invalid (<3 chars). (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
    critical_warnings_exist = True


# ------------- [Environment Variables for Django App] -------------

"""
Set the deployment environment by setting the DEPLOYMENT environment variable.
The default is 'local' if the DEPLOYMENT environment variable is not set.

Options:
    - local: For local development with debugging.
    - development: Tests code in conditions near identical to production. 
        Everything is identical to production except what is required to host locally.
    - production: Production environment for beta testing and release.
"""

#Set the deployment environment.
DEPLOYMENT = os.environ.get('DEPLOYMENT')

# Make deployment environment all lowercase.
if DEPLOYMENT != None:
    DEPLOYMENT = DEPLOYMENT.lower()

# Check that the deployment environment is valid. Otherwise, set it to 'local' and warn the user.
if DEPLOYMENT != 'production' and DEPLOYMENT != 'development' and DEPLOYMENT != 'local':
    DEPLOYMENT = 'local'
    running_deployment_transcript+= red_critical(f'[Critical] DEPLOYMENT environment variable not set. Defaulting to {DEPLOYMENT}. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
    critical_warnings_exist = True

# Set the deployment transcript.
running_deployment_transcript+= f'\n [Logging] Running in {DEPLOYMENT}. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n'


"""
Set the secret_key, debug mode, and allowed hosts based on the 
deployment environment and the environment variables.

Requirements:
    - SECRET_KEY: A secret key for the Django project. 
        [Environment variable in: development, production]
    - DEBUG: A boolean value for whether or not to run in debug mode.
    - ALLOWED_HOSTS: A list of strings representing the allowed hosts. 
        [Environment variable in: development, production]
"""

# Set the secret key.
if DEPLOYMENT == 'local':
    SECRET_KEY = 'django-insecure-davc%f$&u#j!+l_ebeoqd+h^xtz##u)ijf(0yb_ugv^6jh^!t$'
else: # Development and production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Check if valid
    if SECRET_KEY == None or len(SECRET_KEY) < 50: # if invalid
        running_deployment_transcript+= red_critical(f'[Critical] SECRET_KEY environment variable not set or is not sufficient in length. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
        critical_warnings_exist = True

    if "django-insecure" in SECRET_KEY:
        running_deployment_transcript+= yellow_warning(f'[Warning] SECRET_KEY is set to a default "django-insecure" value. This is not recommended for production. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')


# Set the debug mode.
if DEPLOYMENT == 'local':
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    running_deployment_transcript+= yellow_warning(f'[Warning] DEBUG is set to True. This is not recommended for production. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
else: # Development, staging, and production
    DEBUG = False

# Set the allowed hosts.
if DEPLOYMENT == 'local':
    ALLOWED_HOSTS = ['*']
    running_deployment_transcript+= yellow_warning(f'[Warning] ALLOWED_HOSTS is set to ["*"]. This is not recommended for production. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
else: # Development, staging, and production
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')
    # Check if valid
    if len(ALLOWED_HOSTS) == 0: # if invalid
        running_deployment_transcript+= red_critical(f'[Critical] ALLOWED_HOSTS environment variable not working. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
        critical_warnings_exist = True

    if DEPLOYMENT == "production":
        if ALLOWED_HOSTS[0] == '*':
            running_deployment_transcript+= red_critical(f'[Critical] ALLOWED_HOSTS is set to ["*"]. This is highly not recommended for production. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
            critical_warnings_exist = True
        
        # See if localhost or 127.0.0.1 is in the allowed hosts.
        localhost_in_allowed_hosts = False
        for host in ALLOWED_HOSTS:
            if 'localhost' in host or '127.0.0.1' in host or '0.0.0.0' in host:
                if 'localhost' in host and '.' in localhost: # Fix edge case where localhost is in a valid prod url (such as localhostproduct.com)
                    pass
                else:
                    localhost_in_allowed_hosts = True
                    break
        
        if localhost_in_allowed_hosts:
            running_deployment_transcript+= red_critical(f'[Critical] ALLOWED_HOSTS has localhost, 127.0.0.1, or 0.0.0.0. This is highly not recommended for production. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
            critical_warnings_exist = True



"""
Set CSRF_TRUSTED_ORIGINS based upon ALLOWED_HOSTS. Can change in the future.
"""

# Hard code change later
if DEPLOYMENT != 'local':
    CSRF_TRUSTED_ORIGINS=["https://ai4collab.up.railway.app", "https://www.ai4collab.up.railway.app,https://localhost:8080"]
    # for allowed_host in ALLOWED_HOSTS:
    #     CSRF_TRUSTED_ORIGINS.append("https://"+allowed_host)


"""
Set the database based upon the deployment environment and 
the environment variables.

Requirements:
    - DATABASES: Local SQLite3 or Database url for the postgresql database.
        [Environment variable in: development, production]
"""


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if DEPLOYMENT == 'local':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(BASE_DIR / 'db.sqlite3'),
        }
    }

#Note: currently using one database. In future when add staging and/or development servers, this can be expanded to have seperate DBs.
elif DEPLOYMENT == 'development' or DEPLOYMENT == 'production':
    #connect to postgresql database from environment variables
    DATABASES = {
        'default': dj_database_url.config(default=os.getenv('PSQL_DATABASE_URL'))
    }  







SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get("GOOGLE_CLIENT_ID"),
            'secret': os.environ.get("GOOGLE_SECRET_KEY"),
            'key': ''
        }
    }
}




# ------------- [Other Application Settings] -------------

# Application definition

INSTALLED_APPS = [
    'channels',
    'audio',
    'ai4collab',
    "accounts",
    "llm",
    'rest_framework',


    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders', # CORS


    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth',
]

# Important for allauth
SITE_ID = 1


AUTH_USER_MODEL = "accounts.CustomUser"

REST_AUTH = {
    'TOKEN_MODEL': None,
    'SESSION_LOGIN': True,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}



CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_HTTPONLY = True

# SESSION_COOKIE_SECURE = True




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Whitenoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ai4collab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ai4collab.wsgi.application'


ASGI_APPLICATION = 'ai4collab.routing.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

#TODO: deploy better setup for production
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [('localhost', 6379)],
#         },
#     },
# }



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ------------- [Print Results] -------------

# Print divider
print("--------------------------")

# Print the deployment transcript.
print(running_deployment_transcript)

# Print the results of the settings.py deployment.
if critical_warnings_exist:
    print(red_critical(f'Critical warnings exist. Please fix before deploying. ({DEPLOYMENT} deployment)'))
else:
    print(green_success(f'No errors found in settings.py {DEPLOYMENT} deployment.'))
print("\n")

DEPLOYMENT_TRANSCRIPT = running_deployment_transcript
CRIT_WARNINGS_EXIST = critical_warnings_exist


# ------------- [End of File] -------------

