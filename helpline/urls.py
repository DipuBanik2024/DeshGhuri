
from django.urls import path
from .import views as help_views

urlpatterns = [
    path('help_center/', help_views.help_center, name='help_center'),
    path('privacy_policy/', help_views.privacy_policy, name='privacy_policy'),
    path('services/', help_views.services, name='services'),
    path('terms/', help_views.terms, name='terms'),
    path('contact/', help_views.contact_view, name='contact'),

]