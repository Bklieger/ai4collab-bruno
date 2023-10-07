from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout

def custom_google_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    return render(request, 'login.html')

def custom_logout(request):
    logout(request)
    return redirect("/")