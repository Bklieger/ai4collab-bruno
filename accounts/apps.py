"""
Apps.py file for accounts app.

Author(s): Benjamin Klieger
Version: 1.1.0
Date: 2024-01-11
"""

from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
