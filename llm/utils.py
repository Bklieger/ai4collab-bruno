#------- [Import Libraries] -------#
import requests
import os

# Import settings, warning: contains sensitive variables
from django.conf import settings


#------- [Environment Variables] -------#
MIDDLESIGHT_API_KEY = settings.MIDDLESIGHT_API_KEY


#------- [Functions] -------#
def get_llm_feedback(query):
    """
    Get feedback from LLM
    """

    url = "https://ai4c-middle.up.railway.app/api/rapid_chatgpt4_api/"
    headers = {'Authorization': 'Bearer '+str(MIDDLESIGHT_API_KEY), 'Content-Type': 'application/json'}

    payload = {
        "large_string": query,
    }

    response = requests.post(url, headers=headers, json=payload)

    return response.json()["choices"][0]["message"]["content"]
