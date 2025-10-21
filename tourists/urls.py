from django.urls import path
from tourists import views as t_views

urlpatterns = [
    path('home/', t_views.tourist_home, name='tourist_home'),
    path('dashboard/', t_views.tourist_dashboard, name='tourist_dashboard'),  # ✅ ADD THIS
    path('profile/', t_views.tourist_profile, name='tourist_profile'),
    path('profile/edit/', t_views.edit_tourist_profile, name='edit_tourist_profile'),
    path("create_tour_request/", t_views.create_tour_requests, name="create_tour_request"),
    path("notifications/read/", t_views.mark_notifications_read, name="mark_notifications_read"),
]