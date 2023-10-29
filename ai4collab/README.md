# Ai4Collab App

## Details
The Ai4Collab app handles the application settings in settings.py and the deployment status page. A custom command to check the deployment status is also defined under management/commands/env.py

## Environment Variables

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
    - OPENAI_API_KEY: A string representing the OpenAI API key.
        [Environment variable in: local, development, production]

Requirements for each deployment environment:
    Local: GOOGLE_CLIENT_ID, GOOGLE_SECRET_KEY, DJANGO_SETTINGS_MODULE, DEEPGRAM_API_KEY, MIDDLESIGHT_API_KEY or OPENAI_API_KEY required. DEPLOYMENT recommended.
    Development: GOOGLE_CLIENT_ID, GOOGLE_SECRET_KEY, DJANGO_SETTINGS_MODULE, DEPLOYMENT, SECRET_KEY, PSQL_DATABASE_URL, ALLOWED_HOSTS, DEEPGRAM_API_KEY, MIDDLESIGHT_API_KEY or OPENAI_API_KEY required.
    Production: GOOGLE_CLIENT_ID, GOOGLE_SECRET_KEY, DJANGO_SETTINGS_MODULE, DEPLOYMENT, SECRET_KEY, PSQL_DATABASE_URL, ALLOWED_HOSTS, DEEPGRAM_API_KEY, MIDDLESIGHT_API_KEY or OPENAI_API_KEY required.

------- [local.env] --------
DEPLOYMENT=local
DJANGO_SETTINGS_MODULE=ai4collab.settings
DEEPGRAM_API_KEY=<add here>
MIDDLESIGHT_API_KEY=<add here> or OPENAI_API_KEY=<add here>
GOOGLE_CLIENT_ID=<add here>
GOOGLE_SECRET_KEY=<add here>

------- [development.env] --------
DEPLOYMENT=development
DJANGO_SETTINGS_MODULE=ai4collab.settings
SECRET_KEY=<add here>
PSQL_DATABASE_URL=<add here>
ALLOWED_HOSTS=<add here>
DEEPGRAM_API_KEY=<add here>
MIDDLESIGHT_API_KEY=<add here> or OPENAI_API_KEY=<add here>
GOOGLE_CLIENT_ID=<add here>
GOOGLE_SECRET_KEY=<add here>

------- [production.env] --------
DEPLOYMENT=production
DJANGO_SETTINGS_MODULE=ai4collab.settings
SECRET_KEY=<add here>
PSQL_DATABASE_URL=<add here>
ALLOWED_HOSTS=<add here>
DEEPGRAM_API_KEY=<add here>
MIDDLESIGHT_API_KEY=<add here> or OPENAI_API_KEY=<add here>
GOOGLE_CLIENT_ID=<add here>
GOOGLE_SECRET_KEY=<add here>
