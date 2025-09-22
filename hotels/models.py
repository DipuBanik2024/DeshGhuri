from django.db import models
from django.conf import settings

class Hotel(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'role': 'hotel_manager'}, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
