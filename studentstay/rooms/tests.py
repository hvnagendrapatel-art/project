from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import RoomForm
from .models import Room


class RoomPagesTests(TestCase):
    def setUp(self):
        owner = get_user_model().objects.create_user(username="owner", password="testpass123", role="owner")
        self.room = Room.objects.create(owner=owner, title="Test Room", description="A room for testing.", room_type="single", rent=8000, location="Hassan")

    def test_public_room_pages_render(self):
        for url in (reverse("home"), reverse("room-list"), reverse("room-detail", args=[self.room.pk])):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_search_filters_rooms(self):
        response = self.client.get(reverse("room-list"), {"q": "Hassan", "max_rent": "9000"})
        self.assertContains(response, "Test Room")

    def test_room_rent_must_be_below_6000(self):
        invalid_form = RoomForm(data={
            "title": "Test Room",
            "description": "A room for testing.",
            "room_type": "single",
            "rent": 6000,
            "location": "Hassan",
        })
        self.assertFalse(invalid_form.is_valid())
        self.assertIn("rent", invalid_form.errors)

        valid_form = RoomForm(data={
            "title": "Test Room",
            "description": "A room for testing.",
            "room_type": "single",
            "rent": 5999,
            "location": "Hassan",
        })
        self.assertTrue(valid_form.is_valid())

    def test_shared_room_details_are_valid_when_provided(self):
        form = RoomForm(data={
            "title": "Shared Room",
            "description": "A shared room for testing.",
            "room_type": "shared",
            "rent": 5999,
            "location": "Hassan",
            "shared_room_capacity": 3,
        })
        self.assertIn("shared_room_capacity", form.fields)
        self.assertIn("shared_room_price_per_person", form.fields)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["shared_room_capacity"], "3")
        self.assertEqual(form.cleaned_data["shared_room_price_per_person"], 1200)

    def test_shared_room_prices_follow_the_requested_tiers(self):
        for capacity, expected_price in ((2, 2500), (3, 1200), (4, 1000)):
            with self.subTest(capacity=capacity):
                form = RoomForm(data={
                    "title": "Shared Room",
                    "description": "A shared room for testing.",
                    "room_type": "shared",
                    "rent": 5999,
                    "location": "Hassan",
                    "shared_room_capacity": capacity,
                })
                self.assertTrue(form.is_valid(), form.errors)
                self.assertEqual(form.cleaned_data["shared_room_price_per_person"], expected_price)
