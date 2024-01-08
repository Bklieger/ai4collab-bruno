"""
Urls.py file for accounts app.

Author(s): Benjamin Klieger
Version: 1.0.1
Date: 2024-01-07
"""

# Import required libraries for render, redirect, and logout
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout

# View for logging in with google
def custom_google_login(request):
    if request.user.is_authenticated: # If the user is already logged in, redirect to "/". Note: Update "/" if is not the home page.
        return redirect("/")
    return render(request, 'login.html')

# View for logging out
def custom_logout(request):
    logout(request) # Logout the user
    return redirect("/")