from django.contrib import admin
from .models import Hotel, HotelImage, RoomType, HotelBooking, HotelReview, Notification


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        "name", "owner", "city", "area", "average_rating",
        "min_price", "max_price", "created_at"
    )
    list_filter = ("city", "area", "has_wifi", "has_pool", "has_ac", "has_parking")
    search_fields = ("name", "city", "area", "landmark", "owner__username")
    readonly_fields = ("average_rating", "created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        ("Basic Info", {
            "fields": ("owner", "name", "profile_image", "address", "phone", "description")
        }),
        ("Location", {
            "fields": ("city", "area", "landmark")
        }),
        ("Amenities", {
            "fields": ("has_wifi", "has_pool", "has_ac", "has_breakfast", "has_parking", "has_gym")
        }),
        ("Price & Ratings", {
            "fields": ("min_price", "max_price", "average_rating")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )


@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ("hotel", "caption", "created_at")
    search_fields = ("hotel__name", "caption")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ("hotel", "name", "capacity", "price_per_night", "available_rooms")
    list_filter = ("has_ac", "has_tv", "has_balcony")
    search_fields = ("hotel__name", "name")
    ordering = ("hotel", "name")


@admin.register(HotelBooking)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = (
        "id", "tourist", "hotel", "room_type",
        "check_in", "check_out", "status", "total_amount"
    )
    list_filter = ("status", "check_in", "check_out")
    search_fields = ("hotel__name", "tourist__username", "guest_name", "guest_email")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(HotelReview)
class HotelReviewAdmin(admin.ModelAdmin):
    list_display = ("hotel", "tourist", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("hotel__name", "tourist__username", "comment")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "booking", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("user__username", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
