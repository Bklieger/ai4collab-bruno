"""
urls.py file for llm app.

Author(s): Benjamin Klieger
Version: 1.0.1
Date: 2024-01-06
"""

# Django imports
from django.urls import path

# Import view of LLM
from .views import LlmView

urlpatterns = [
    path('api/llm/', LlmView.as_view(), name='llm'), # LLM view
]
