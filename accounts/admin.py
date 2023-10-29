"""
Admin.py file for accounts app.

Author(s): Benjamin Klieger
Version: 1.0.0
Date: 2023-10-26
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Import the CustomUser model
from .models import CustomUser

# Custom Display of Email and Username in Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["email", "username",]

# Register Custom User Model to Admin
admin.site.register(CustomUser, CustomUserAdmin)