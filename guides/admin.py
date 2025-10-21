from django.contrib import admin
from .models import GuideProfile, TourRequest, Tour, Earning, Review


@admin.register(GuideProfile)
class GuideProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'phone', 'experience_years', 'is_verified',
        'average_rating', 'is_completed'
    )
    list_filter = ('is_verified', 'is_completed')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone', 'languages')
    readonly_fields = ('average_rating',)
    fieldsets = (
        ("User Information", {
            "fields": ('user', 'phone', 'avatar', 'bio', 'languages', 'address')
        }),
        ("Experience", {
            "fields": ('experience_years', 'is_verified', 'average_rating', 'is_completed')
        }),
    )


@admin.register(TourRequest)
class TourRequestAdmin(admin.ModelAdmin):
    list_display = (
        'tourist', 'guide', 'destination', 'date', 'number_of_travelers',
        'duration_hours', 'price', 'status', 'created_at'
    )
    list_filter = ('status', 'date', 'duration_hours')
    search_fields = ('tourist__username', 'guide__username', 'destination')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ("Basic Info", {
            "fields": ('tourist', 'guide', 'destination', 'date', 'places_to_explore')
        }),
        ("Details", {
            "fields": ('number_of_travelers', 'duration_hours', 'price', 'notes')
        }),
        ("Status", {
            "fields": ('status', 'created_at')
        }),
    )


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = (
        'guide', 'destination', 'start_date', 'end_date', 'price', 'status'
    )
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('guide__username', 'destination')
    filter_horizontal = ('tourists',)
    fieldsets = (
        ("Tour Info", {
            "fields": ('guide', 'tourists', 'destination', 'start_date', 'end_date')
        }),
        ("Details", {
            "fields": ('price', 'status', 'notes')
        }),
    )


@admin.register(Earning)
class EarningAdmin(admin.ModelAdmin):
    list_display = ('guide', 'amount', 'description', 'date')
    list_filter = ('date',)
    search_fields = ('guide__username', 'description')
    ordering = ('-date',)
    readonly_fields = ('date',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('tourist', 'guide', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('tourist__username', 'guide__username', 'comment')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
