"""
urls.py file for llm app.

Author(s): Benjamin Klieger
Version: 1.1.0
Date: 2024-01-07
"""

# Django imports
from django.urls import path

# Import view of LLM
from .views import LlmView

urlpatterns = [
    path('api/llm/', LlmView.as_view(), name='llm'), # LLM view
]
