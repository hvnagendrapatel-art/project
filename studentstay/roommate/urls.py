from django.urls import path
from . import views

urlpatterns = [
    path("", views.RoommateListView.as_view(), name="roommate-list"),
    path("new/", views.RoommateCreateView.as_view(), name="roommate-create"),
    path("<int:pk>/", views.RoommateDetailView.as_view(), name="roommate-detail"),
    path("<int:pk>/edit/", views.RoommateUpdateView.as_view(), name="roommate-update"),
    path("<int:pk>/delete/", views.RoommateDeleteView.as_view(), name="roommate-delete"),
]
