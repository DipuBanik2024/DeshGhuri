from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.guide_dashboard, name='guide_dashboard'),
    path('dashboard/edit/', views.edit_guide_profile, name='edit_guide_profile'),
]
