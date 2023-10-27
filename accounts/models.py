"""
Models.py file for accounts app.

Author(s): Benjamin Klieger
Version: 1.0.0
Date: 2023-10-26
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class CustomUser(AbstractUser):
    pass
    # Additional fields can be added here

    def __str__(self):
        return self.username