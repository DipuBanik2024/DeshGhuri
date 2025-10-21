from django.urls import path
from . import views as h_views

urlpatterns = [
    # Public hotel views
    path("", h_views.hotels_info, name="hotels_info"),
    path("<int:hotel_id>/", h_views.hotel_detail, name="hotel_detail"),

    # Hotel reviews (direct - no booking required)
    path("<int:hotel_id>/review/", h_views.submit_hotel_review, name="submit_hotel_review"),

    # Hotel management (owner only)
    path("dashboard/", h_views.hotel_dashboard, name="hotel_dashboard"),
    path("create/", h_views.hotel_create, name="hotel_create"),
    path("<int:pk>/edit/", h_views.hotel_edit, name="hotel_edit"),
    path("<int:pk>/delete/", h_views.hotel_delete, name="hotel_delete"),
    path("<int:hotel_id>/rooms/", h_views.manage_rooms, name="manage_rooms"),

    # Room type management
    path("<int:hotel_id>/rooms/<int:room_type_id>/edit/", h_views.room_type_edit, name="room_type_edit"),
    path("<int:hotel_id>/rooms/<int:room_type_id>/delete/", h_views.room_type_delete, name="room_type_delete"),

    # Hotel images management
    path("<int:hotel_id>/images/", h_views.manage_hotel_images, name="manage_hotel_images"),
    path("<int:hotel_id>/images/<int:image_id>/delete/", h_views.delete_hotel_image, name="delete_hotel_image"),

    # Booking management
    path("book/<int:hotel_id>/<int:room_type_id>/", h_views.book_hotel, name="book_hotel"),
    path("booking/<int:booking_id>/review/", h_views.submit_review, name="submit_review"),
    path("booking/<int:booking_id>/<str:status>/", h_views.update_booking_status, name="update_booking_status"),
    path("booking/<int:booking_id>/detail/", h_views.booking_detail, name="booking_detail"),

    # Review management (update/delete)
    path("review/<int:review_id>/edit/", h_views.edit_review, name="edit_hotel_review"),
    path("review/<int:review_id>/delete/", h_views.delete_review, name="delete_hotel_review"),
    path("my-reviews/", h_views.my_reviews, name="my_reviews"),

    # Notifications
    path("notifications/", h_views.my_notifications, name="my_notifications"),
    path("notifications/<int:notification_id>/read/", h_views.mark_notification_read, name="mark_notification_read"),
    path("notifications/mark-all-read/", h_views.mark_hotel_notifications_read, name="mark_hotel_notifications_read"),

    # API
    path("api/search/", h_views.hotel_search_api, name="hotel_search_api"),
]