from django.db import models
from accounts.models import CustomUser
from datetime import datetime, timedelta

class RequestLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    prompt = models.TextField()
    response = models.TextField()

    @classmethod
    def count_requests_in_last_24_hours(cls):
        return cls.objects.filter(timestamp__gte=datetime.now()-timedelta(hours=24)).count()

    @classmethod
    def count_requests_in_last_24_hours_for_user(cls, user):
        return cls.objects.filter(user=user, timestamp__gte=datetime.now()-timedelta(hours=24)).count()
    
    @classmethod
    def count_requests_in_last_n_hours_for_user(cls, user=None, n=None):
        if user is None:
            return cls.objects.filter(timestamp__gte=datetime.now()-timedelta(hours=n)).count()

        if n is None:
            return cls.objects.filter(user=user).count()

        if user is not None and n is not None:
            return cls.objects.filter(user=user, timestamp__gte=datetime.now()-timedelta(hours=n)).count()
        
        raise Exception("Invalid parameters for count_requests_in_last_n_hours_for_user")