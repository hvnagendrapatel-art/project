from django.conf import settings
from django.db import models
from django.urls import reverse


class RoommatePost(models.Model):
    GENDER_CHOICES = [("", "No preference"), ("female", "Female"), ("male", "Male"), ("any", "Any")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="roommate_posts")
    preferred_location = models.CharField(max_length=200)
    budget = models.PositiveIntegerField()
    has_room = models.BooleanField(default=False, help_text="Select this if you already have a room and need a roommate.")
    room_details = models.TextField(blank=True, help_text="Optional: room type, rent split, amenities, or other useful details.")
    move_in_date = models.DateField(null=True, blank=True)
    gender_preference = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    bio = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} — {self.preferred_location}"

    def get_absolute_url(self):
        return reverse("roommate-detail", kwargs={"pk": self.pk})
