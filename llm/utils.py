"""
utils.py file for llm app. Define request to LLM API for
chat with Bruno.

Author(s): Benjamin Klieger
Version: 1.0.0
Date: 2023-10-26
"""

#------- [Import Libraries] -------#
import requests
import os

# Import settings, warning: contains sensitive variables
from django.conf import settings


#------- [Environment Variables] -------#
MIDDLESIGHT_API_KEY = settings.MIDDLESIGHT_API_KEY
OPENAI_API_KEY = settings.OPENAI_API_KEY


#------- [Define Variables] -------#
url = "https://ai4c-middle.up.railway.app/api/rapid_chatgpt4_api/"


#------- [Functions] -------#
def get_llm_feedback(query: str) -> str:
    """
    Get feedback from LLM using OpenAI, or if not available, MiddleSight.

    Args:
        query (string): The prompt to send to LLM.

    Returns:
        string: The response from LLM.
    """

    if OPENAI_API_KEY == None:
        #Use Middlesight API
        headers = {'Authorization': 'Bearer '+str(MIDDLESIGHT_API_KEY), 'Content-Type': 'application/json'}

        payload = {
            "large_string": query,
        }

        response = requests.post(url, headers=headers, json=payload)

        return response.json()["choices"][0]["message"]["content"]

    else:
        #Use OpenAI API
        headers = {'Authorization': 'Bearer '+str(OPENAI_API_KEY), 'Content-Type': 'application/json'}

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": query}],
            "temperature": 0.7
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        return response.json()["choices"][0]["message"]["content"]