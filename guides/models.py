from django.db import models
from django.conf import settings

class GuideProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Guide: {self.user.get_full_name() or self.user.username}"
