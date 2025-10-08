from django.db import models
from django.conf import settings

class Tourist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tourist_profile')

    # Personal Information
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='tourist_profiles/', blank=True, null=True)
    address = models.TextField(blank=True)

    # Travel Preferences
    TRAVEL_STYLES = [
        ('ADVENTURE', 'Adventure Seeker'),
        ('LUXURY', 'Luxury Traveler'),
        ('BUDGET', 'Budget Backpacker'),
        ('FAMILY', 'Family Traveler'),
        ('SOLO', 'Solo Traveler'),
        ('CULTURAL', 'Cultural Explorer'),
    ]
    travel_style = models.CharField(max_length=20, choices=TRAVEL_STYLES, blank=True)

    # Optional profile completion flag
    is_completed = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tourist: {self.user.get_full_name() or self.user.username}"
