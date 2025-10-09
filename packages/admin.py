from django.contrib import admin
from .models import Package, Booking, Review

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('destination_name', 'price', 'people_limit')
    search_fields = ('destination_name',)
    list_filter = ('price',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('package', 'tourist', 'booking_date', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('tourist__username', 'package__destination_name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('package', 'tourist', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('tourist__username', 'package__destination_name')
