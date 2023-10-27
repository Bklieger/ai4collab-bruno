"""
views.py file for ai4collab app. Define deployment status page.

Author(s): Benjamin Klieger
Version: 1.0.0
Date: 2023-10-26
"""

#------- [Import Libraries] -------#
# Import Django render and Http404
from django.shortcuts import render
from django.http import Http404

# Import settings, Warning: contains sensitive variables
from django.conf import settings


#------- [Environment Variables] -------#
running_deployment_transcript = settings.DEPLOYMENT_TRANSCRIPT # String
critical_warnings_exist = settings.CRIT_WARNINGS_EXIST # Boolean


#------- [Define Views] -------#
# View for deployment status page
def deployment_status(request):
    #ensure user is superadmin
    if not request.user.is_superuser:
        raise Http404 # If not superadmin, raise 404 error
    
    # Render deployment status page and pass in environment variables
    return render(request, 'deployment_status.html', {'running_deployment_transcript': running_deployment_transcript, 'critical_warnings_exist': critical_warnings_exist})

