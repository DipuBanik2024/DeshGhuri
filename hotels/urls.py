from django.urls import path
from hotels.views import hotels_info, hotel_dashboard, hotel_create, hotel_edit, hotel_delete

urlpatterns = [
    path("hotels/", hotels_info, name="hotels_info"),
    path("hotels/dashboard/", hotel_dashboard, name="hotel_dashboard"),
    path("hotels/create/", hotel_create, name="hotel_create"),
    path("hotels/<int:pk>/edit/", hotel_edit, name="hotel_edit"),
    path("hotels/<int:pk>/delete/", hotel_delete, name="hotel_delete"),
]
