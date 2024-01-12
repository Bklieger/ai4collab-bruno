"""
urls.py file for llm app.

Author(s): Benjamin Klieger
Version: 1.1.0
Date: 2024-01-11
"""

# Django imports
from django.urls import path

# Import view of LLM
from .views import LlmView, LlmOnlyView

urlpatterns = [
    path('api/llm/', LlmView.as_view(), name='llm'), # LLM view
    path('api/llm_only/', LlmOnlyView.as_view(), name='llm_only'), # LLM view
]
