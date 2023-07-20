#------- [Import Libraries] -------#

# Django
from django.shortcuts import render

# Import settings, warning: contains sensitive variables
from django.conf import settings


#------- [Environment Variables] -------#
running_deployment_transcript = settings.DEPLOYMENT_TRANSCRIPT # String
critical_warnings_exist = settings.CRIT_WARNINGS_EXIST # Boolean



def deployment_status(request):
    return render(request, 'deployment_status.html', {'running_deployment_transcript': running_deployment_transcript, 'critical_warnings_exist': critical_warnings_exist})