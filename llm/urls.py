"""
urls.py file for llm app.
live transcription.

Author(s): Benjamin Klieger
Version: 1.0.0
Date: 2023-10-26
"""

# Django imports
from django.urls import path

# Import view of LLM
from .views import LlmView

urlpatterns = [
    path('api/llm/', LlmView.as_view(), name='llm'), # LLM view
]