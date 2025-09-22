# destination/models.py
from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)

    def __str__(self):
        return self.name
