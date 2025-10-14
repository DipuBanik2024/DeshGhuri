from django.urls import path
from . import views as g_views

urlpatterns = [
    path('dashboard/', g_views.guide_dashboard, name='guide_dashboard'),
    path("profile/", g_views.guide_profile, name="guide_profile"),
    path('edit_profile/', g_views.edit_guide_profile, name='edit_profile'),
    path("tour_requests/", g_views.tour_requests, name="tour_requests"),
    path("guides/", g_views.guide_list, name="guide_list"),
    path("guides/<int:guide_id>/", g_views.guide_detail, name="guide_detail"),
    path('tour-requests/accept/<int:request_id>/', g_views.accept_request, name='accept_request'),
    path('tour-requests/reject/<int:request_id>/', g_views.reject_request, name='reject_request'),
    path("my_tours/", g_views.my_tours, name="my_tours"),
    path("earnings/", g_views.earnings, name="earnings"),
    path("messages/", g_views.guide_messages, name="guide_messages"),

    # NEW REVIEW URLS
    path("guides/<int:guide_id>/review/create/", g_views.create_review, name="create_review"),
    path("reviews/<int:review_id>/edit/", g_views.edit_review, name="edit_review"),
    path("reviews/<int:review_id>/delete/", g_views.delete_review, name="delete_review"),

    # NEW BOOKING URL
    path("guides/<int:guide_id>/book/", g_views.book_guide, name="book_guide"),
]