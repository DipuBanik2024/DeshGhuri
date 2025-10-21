from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Hotel(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'role': 'hotel_manager'},
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)

    # Image fields
    profile_image = models.ImageField(upload_to='hotel_profile_images/', blank=True, null=True,
                                      help_text="Main image for hotel cards and listings")

    # Location details for filtering
    city = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    landmark = models.CharField(max_length=200, blank=True)

    # Rating
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    # Amenities for filtering
    has_wifi = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_ac = models.BooleanField(default=False)
    has_breakfast = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)

    # Price range
    min_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def update_price_range(self):
        """Update min and max price based on room types"""
        room_prices = self.room_types.all().values_list('price_per_night', flat=True)
        if room_prices:
            self.min_price = min(room_prices)
            self.max_price = max(room_prices)
            self.save()


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='hotel_gallery/')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.hotel.name}"


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=100)  # "Single Room", "Double Room", "Suite", etc.
    description = models.TextField(blank=True)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available_rooms = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    room_image = models.ImageField(upload_to='room_images/', blank=True, null=True,
                                   help_text="Image for this room type")

    # Room amenities
    has_ac = models.BooleanField(default=False)
    has_tv = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    room_size = models.CharField(max_length=50, blank=True)  # "25 sqm", "40 sqm", etc.

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"


class HotelBooking(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    tourist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hotel_bookings')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='bookings')

    # Booking details
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_rooms = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    total_guests = models.IntegerField(validators=[MinValueValidator(1)], default=1)

    # Pricing
    room_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Status
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')

    # Contact info
    guest_name = models.CharField(max_length=200)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)
    special_requests = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.hotel.name}"


class HotelReview(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    tourist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hotel_reviews')
    booking = models.ForeignKey(HotelBooking, on_delete=models.CASCADE, related_name='review', null=True, blank=True)

    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['hotel', 'tourist']


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    booking = models.ForeignKey(HotelBooking, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"