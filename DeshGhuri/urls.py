"""
URL configuration for DeshGhuri project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include

from hotels.views import hotels_info
from main import views as main_views
from accounts import views as a_views
from destinations import views as d_views
from helpline import views as h_views
from guides import views as g_views
from hotels import views as hotels_views
from packages import views as p_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # accounts app routes
    #main
    path('',main_views.home,name='home'),

    #helpline
    path('help_center',h_views.help_center,name='help_center'),
    #guides
    path('guides_info',g_views.guides_info,name='guides_info'),
    #hotels
    path('hotels_info',hotels_views.hotels_info,name="hotels_info"),
    #packages
    path('packages_info',p_views.packages_info,name='packages_info'),

    path('accounts/', include('accounts.urls')),
    path('guides/', include('guides.urls')),
    path('hotels/', include('hotels.urls')),
    path('destinations/', include('destinations.urls')),
]
