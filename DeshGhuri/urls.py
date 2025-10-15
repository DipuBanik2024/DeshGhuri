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
from . import settings
from django.conf.urls.static import static
from django.urls import path, include

from hotels.views import hotels_info
from main import views as main_views
from accounts import views as a_views
from destinations import views as d_views
from helpline import views as h_views
from guides import views as g_views
from hotels import views as hotels_views
from packages import views as p_views
from tourists import views as t_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # accounts app routes
    #main
    path('',main_views.home,name='home'),

    #helpline

    #hotels
    path('hotels_info',hotels_views.hotels_info,name="hotels_info"),
    #packages

    path('accounts/', include('accounts.urls')),
    path('guides/', include('guides.urls')),
    path('hotels/', include('hotels.urls')),
    path('packages/', include('packages.urls')),
    path('destinations/', include('destinations.urls')),
    path('tourists/', include('tourists.urls')),
    path('helpline/', include('helpline.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
