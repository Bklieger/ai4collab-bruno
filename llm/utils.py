"""
utils.py file for llm app. Define request to LLM API for
chat with Bruno.

Author(s): Benjamin Klieger
Version: 1.1.0
Date: 2024-01-11
"""

#------- [Import Libraries] -------#
import requests
import os

# Import settings, warning: contains sensitive variables
from django.conf import settings


#------- [Environment Variables] -------#
OPENAI_API_KEY = settings.OPENAI_API_KEY


#------- [Functions] -------#
def get_llm_feedback(query: str) -> str:
    """
    Get feedback from LLM using OpenAI.

    Args:
        query (string): The prompt to send to LLM.

    Returns:
        string: The response from LLM.
    """

    #Use OpenAI API
    headers = {'Authorization': 'Bearer '+str(OPENAI_API_KEY), 'Content-Type': 'application/json'}

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": query}],
        "temperature": 0.7
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()["choices"][0]["message"]["content"]