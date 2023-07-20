from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model
class CustomUser(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username