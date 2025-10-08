from django.urls import path
from tourists import views as t_views

urlpatterns = [
    path('dashboard/', t_views.tourist_dashboard, name='tourist_dashboard'),
    path('profile/', t_views.tourist_profile, name='tourist_profile'),
    path('profile/edit/', t_views.edit_tourist_profile, name='edit_tourist_profile'),

    #path('dashboard/edit/', t_views.dashboard_edit, name='dashboard_edit'),
    path("create_tour_request/", t_views.create_tour_requests, name="create_tour_request"),


]

