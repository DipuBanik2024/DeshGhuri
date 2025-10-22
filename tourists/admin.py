from django.contrib import admin
from .models import Tourist

@admin.register(Tourist)
class TouristAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'travel_style', 'is_completed', 'created_at')
    list_filter = ('travel_style', 'is_completed', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'profile_picture', 'bio', 'is_completed')
        }),
        ('Personal Details', {
            'fields': ('phone_number', 'date_of_birth', 'address')
        }),
        ('Travel Preferences', {
            'fields': ('travel_style',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
