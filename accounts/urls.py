from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client


class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://localhost:8000/accounts/dj-rest-auth/google/'
    client_class = OAuth2Client

from django.urls import path
from . import views  # Adjust the import based on your views.py location


urlpatterns = [
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('login/', views.custom_google_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
]
