from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # default validator remove kore sudhu max_length r unique thakbe
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer."
    )

    ROLE_CHOICES = (
        ('tourist', 'Tourist'),
        ('guide', 'Guide'),
        ('hotel_manager', 'Hotel Manager'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


    def is_tourist(self):
        return self.role == 'tourist'

    def is_guide(self):
        return self.role == 'guide'

    def is_hotel_manager(self):
        return self.role == 'hotel_manager'
