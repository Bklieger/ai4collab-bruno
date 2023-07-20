from django.urls import path

from .views import LlmView

urlpatterns = [
    path('api/llm/', LlmView.as_view(), name='llm'),
]