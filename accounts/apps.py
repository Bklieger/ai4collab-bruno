"""
Apps.py file for accounts app.

Author(s): Benjamin Klieger
Version: 1.0.0
Date: 2023-10-26
"""

from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
