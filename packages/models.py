from django.db import models
from django.conf import settings  # 🔥 Import this to use custom user model
from django.db.models import Avg

class Package(models.Model):
    destination_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='package_images/')
    people_limit = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    days = models.PositiveIntegerField(default=1)  # নতুন field: Tour কত দিন
    description = models.TextField()
    itinerary = models.TextField()
    included_services = models.TextField()
    exclusions = models.TextField()

    def __str__(self):
        return self.destination_name
        # ✅ New method for average rating

    def average_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else None

        # ✅ Optional: total number of reviews

    def review_count(self):
        return self.reviews.count()


class Booking(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    tourist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    people_count = models.PositiveIntegerField(default=1)   # tourist কতজন আসবে
    tour_date = models.DateField(null=True, blank=True)     # tour-এর date
    mobile_number = models.CharField(max_length=15, null=True, blank=True)  # নতুন field
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.tourist} - {self.package.destination_name}"


class Review(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='reviews')
    tourist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ✅ fixed
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tourist} - {self.package.destination_name}"
