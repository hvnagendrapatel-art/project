from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("owners/", views.owner_portal, name="owner-portal"),
    path("rooms/", views.RoomListView.as_view(), name="room-list"),
    path("rooms/new/", views.RoomCreateView.as_view(), name="room-create"),
    path("rooms/<int:pk>/", views.RoomDetailView.as_view(), name="room-detail"),
    path("rooms/<int:pk>/edit/", views.RoomUpdateView.as_view(), name="room-update"),
    path("rooms/<int:pk>/delete/", views.RoomDeleteView.as_view(), name="room-delete"),
    path("rooms/<int:pk>/save/", views.toggle_wishlist, name="toggle-wishlist"),
    path("rooms/<int:pk>/rental-status/", views.toggle_rental_status, name="toggle-rental-status"),
    path("rooms/<int:pk>/review/", views.create_review, name="review-create"),
]
