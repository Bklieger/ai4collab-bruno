"""
Django settings for ai4collab project.

Environmental Variables:
    - DEPLOYMENT: A string representing the deployment environment.
        [Options: local, development, production]
    - SECRET_KEY: A secret key for the Django project.
        [Environment variable in: production]
    - DEBUG: A boolean value for whether or not to run in debug mode.
    - ALLOWED_HOSTS: A list of strings representing the allowed hosts.
        [Environment variable in: development, production]
    - PSQL_DATABASE_URL: A string representing the database URL.
        [Environment variable in: development, production]

Requirements for each deployment environment:
    Local: None required. DEPLOYMENT recommended.
    Development: DEPLOYMENT, SECRET_KEY, PSQL_DATABASE_URL, ALLOWED_HOSTS required.
    Production: DEPLOYMENT, SECRET_KEY, PSQL_DATABASE_URL, ALLOWED_HOSTS required.

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


# ------------- [Environmental Variables] -------------

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
deployment environment and the environmental variables.

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
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')
    # Check if valid
    if len(ALLOWED_HOSTS) == 0: # if invalid
        running_deployment_transcript+= red_critical(f'[Critical] ALLOWED_HOSTS environment variable not working. (Line {inspect.currentframe().f_lineno} in {os.path.basename(__file__)})\n')
        critical_warnings_exist = True


"""
Set the database based upon the deployment environment and 
the environmental variables.

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



# ------------- [Other Application Settings] -------------

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ai4collab',
    'audio',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Whitenoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
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

# ------------- [End of File] -------------

