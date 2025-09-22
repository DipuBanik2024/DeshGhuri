
from django.urls import path
from accounts import views as a_views

urlpatterns = [
    path('signup/', a_views.signup_view, name='signup'),
    path('login/', a_views.login_view, name='login'),
    path('logout/', a_views.logout_view, name='logout'),
    path('dashboard/', a_views.dashboard_view, name='dashboard'),


]
