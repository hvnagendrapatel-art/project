from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Room(models.Model):
    ROOM_TYPES = [("single", "Single"), ("shared", "Shared"), ("pg", "PG")]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="rooms")
    title = models.CharField(max_length=200)
    description = models.TextField()
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    rent = models.PositiveIntegerField()
    shared_room_capacity = models.PositiveIntegerField(null=True, blank=True, help_text="How many people can share this room")
    shared_room_price_per_person = models.PositiveIntegerField(null=True, blank=True, help_text="Price per person for shared rooms")
    location = models.CharField(max_length=200)
    college_nearby = models.CharField(max_length=150, blank=True)
    distance_from_college = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="Distance in kilometres")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("room-detail", kwargs={"pk": self.pk})

    @property
    def shared_price_display(self):
        if self.room_type != "shared" or not self.shared_room_capacity:
            return None
        price_map = {2: 2500, 3: 1200, 4: 1000}
        return price_map.get(int(self.shared_room_capacity))


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="rooms/")


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlisted_rooms")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="wishlist_entries")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "room"], name="unique_wishlist_room")]


class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["room", "user"], name="unique_room_review")]
