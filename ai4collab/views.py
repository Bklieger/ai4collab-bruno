"""
views.py file for ai4collab app. Define deployment status page.

Author(s): Benjamin Klieger
Version: 1.1.0
Date: 2024-01-11
"""

#------- [Import Libraries] -------#
# Import Django render and Http404
from django.shortcuts import render
from django.http import Http404

# Import settings, Warning: contains sensitive variables
from django.conf import settings

# Import Regular Expressions
import re

#------- [Environment Variables] -------#
running_deployment_transcript = settings.DEPLOYMENT_TRANSCRIPT # String
critical_warnings_exist = settings.CRIT_WARNINGS_EXIST # Boolean


#------- [Initialization] -------#
# Replace \x1b\[93m with newline
running_deployment_transcript = re.sub(r'\x1b\[93m', '\n', running_deployment_transcript)

# Replace \x1b\[92m with newline
running_deployment_transcript = re.sub(r'\x1b\[92m', '\n', running_deployment_transcript)

# Replace \x1b\[91m with newline
running_deployment_transcript = re.sub(r'\x1b\[91m', '\n', running_deployment_transcript)

# Replace \x1b\[91m with newline
running_deployment_transcript = re.sub(r'\x1b\[0m', '\n', running_deployment_transcript)


#------- [Define Views] -------#
# View for deployment status page
def deployment_status(request):
    #ensure user is superadmin
    if not request.user.is_superuser:
        raise Http404 # If not superadmin, raise 404 error
    
    # Turn into array seperated by newlines
    transcript = running_deployment_transcript.split('\n')

    # Render deployment status page and pass in environment variables
    return render(request, 'deployment_status.html', {'running_deployment_transcript': transcript, 'critical_warnings_exist': critical_warnings_exist})
