"""
Env.py file for ai4collab app. This file defines a custom 
command that will allow the user to check with deployment 
environment they are currently using.

Author(s): Benjamin Klieger
Version: 1.0.0
Date: 2023-10-26
"""

# Import required libraries
from django.core.management.base import BaseCommand, CommandError
import os # For checking the environment variable

# Define the command
class Command(BaseCommand):
    # Help message for the command
    help = 'Command to view the current deployment environment'

    def handle(self, *args, **options):
        #From Settings.py, Should be Kept Identical
        # ------------- [Deployment Environment] -------------
        
        #Set the deployment environment.
        DEPLOYMENT = os.environ.get('DEPLOYMENT')

        # Make deployment environment all lowercase.
        if DEPLOYMENT != None:
            DEPLOYMENT = DEPLOYMENT.lower()

        # Check that the deployment environment is valid. Otherwise, set it to 'local' and warn the user.
        if DEPLOYMENT != 'production' and DEPLOYMENT != 'development' and DEPLOYMENT != 'local':
            DEPLOYMENT = 'local'
            self.stdout.write('Warning, no deployment environment found. Defaulting to local.')
        else:
            self.stdout.write(f'Deployment environment is {DEPLOYMENT}.')