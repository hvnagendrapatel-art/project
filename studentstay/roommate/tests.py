from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import RoommatePost


class RoommatePagesTests(TestCase):
    def test_roommate_list_renders(self):
        user = get_user_model().objects.create_user(username="student", password="testpass123")
        RoommatePost.objects.create(user=user, preferred_location="Hassan", budget=7000, bio="Looking for a clean roommate.")
        response = self.client.get(reverse("roommate-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "student")
