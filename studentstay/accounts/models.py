from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("owner", "Property Owner"),
    ]

    phone = models.CharField(max_length=15, blank=True)
    college = models.CharField(max_length=150, blank=True)
    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student"
    )

    def __str__(self):
        return self.username