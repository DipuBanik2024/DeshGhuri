
from django.urls import path
from .import views as h_views

urlpatterns = [
    path('help_center/', h_views.help_center, name='help_center'),
    path('privacy_policy/', h_views.privacy_policy, name='privacy_policy'),
    path('services/', h_views.services, name='services'),
    path('terms/', h_views.terms, name='terms'),
    path('contact/', h_views.contact_view, name='contact'),

]