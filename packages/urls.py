from django.urls import path
from . import views

urlpatterns = [
    path('', views.package_list, name='package_list'),
    path('<int:pk>/', views.package_detail, name='package_detail'),
    path('<int:pk>/book/', views.book_package, name='book_package'),
    path('<int:pk>/review/', views.add_review, name='add_review'),
]
