from django.db import models
from django.conf import settings

class GuideProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(upload_to='guides/avatars/', blank=True)
    is_verified = models.BooleanField(default=False)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    # Future-proof fields
    languages = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)

    # Optional profile completion flag
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Guide: {self.user.get_full_name() or self.user.username}"

class TourRequest(models.Model):
    tourist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tourist_requests")
    guide = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="guide_requests", null=True, blank=True)
    destination = models.CharField(max_length=200)
    date = models.DateField()
    notes = models.TextField(blank=True)
    # নতুন price ফিল্ড যোগ করুন
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Proposed Price"
    )
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("accepted", "Accepted"), ("completed", "Completed"), ("rejected", "Rejected")],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)  # এটি থাকলে ভালো

    def __str__(self):
        return f"{self.tourist} → {self.destination} ({self.status})"


class Tour(models.Model):
    guide = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="guide_tours")
    tourists = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tours")
    destination = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("ongoing", "Ongoing"), ("completed", "Completed")],
        default="pending"
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Tour at {self.destination} ({self.status})"


class Earning(models.Model):
    guide = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="earnings")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)  # এই লাইন যোগ করুন
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guide} earned {self.amount}"