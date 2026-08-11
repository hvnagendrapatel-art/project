from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from roommate.models import RoommatePost
from rooms.models import Review, Room, Wishlist


class Command(BaseCommand):
    help = "Create demo users, room listings, roommate profiles, saved rooms, and reviews."

    def handle(self, *args, **options):
        User = get_user_model()
        owner, _ = User.objects.get_or_create(username="demo_owner", defaults={"email": "owner@studentstay.local", "role": "owner", "college": "Malnad College of Engineering", "phone": "9876543210"})
        owner.set_password("demo12345")
        owner.save()
        sukruth, _ = User.objects.get_or_create(username="sukruth", defaults={"email": "sukruth@stayfinder.local", "college": "Malnad College of Engineering", "phone": "9876543211"})
        sukruth.set_password("demo12345")
        sukruth.save()
        darshan, _ = User.objects.get_or_create(username="darshan", defaults={"email": "darshan@stayfinder.local", "college": "Government Engineering College, Hassan", "phone": "9876543212"})
        darshan.set_password("demo12345")
        darshan.save()

        room_data = [
            ("Sunrise Student PG", "Comfortable single room in a secure student PG with Wi-Fi, hot water, meals and study space.", "single", 6500, "Vijayanagar, Hassan", "Malnad College of Engineering", 0.6),
            ("Greenview Shared Flat", "A bright two-bedroom shared flat. The rent includes Wi-Fi and housekeeping.", "shared", 4500, "B.M. Road, Hassan", "Malnad College of Engineering", 1.2),
            ("Campus Corner PG", "Well-maintained PG close to bus stops and shops. Separate floors and CCTV security.", "pg", 7500, "Sanjay Nagar, Hassan", "Malnad College of Engineering", 0.4),
            ("Lakeview Single Room", "Quiet furnished room suitable for focused study. Attached bathroom and parking available.", "single", 5800, "Kuvempu Nagar, Hassan", "Government Engineering College, Hassan", 1.8),
        ]
        rooms = []
        for title, description, room_type, rent, location, college, distance in room_data:
            defaults = {"description": description, "room_type": room_type, "rent": rent, "location": location, "college_nearby": college, "distance_from_college": distance}
            if room_type == "shared":
                defaults.update({"shared_room_capacity": 3, "shared_room_price_per_person": 1200})
            room, _ = Room.objects.update_or_create(title=title, owner=owner, defaults=defaults)
            rooms.append(room)

        RoommatePost.objects.get_or_create(user=sukruth, preferred_location="Vijayanagar, Hassan", defaults={"budget": 7000, "gender_preference": "female", "bio": "CSBS student looking for a tidy, friendly roommate. I enjoy cooking and quiet study evenings."})
        RoommatePost.objects.get_or_create(user=darshan, preferred_location="B.M. Road, Hassan", defaults={"budget": 6500, "gender_preference": "any", "bio": "Engineering student looking to share a flat near campus. I am easy-going and keep shared spaces clean."})
        Wishlist.objects.get_or_create(user=sukruth, room=rooms[0])
        Review.objects.get_or_create(room=rooms[0], user=sukruth, defaults={"rating": 5, "comment": "Clean room and the owner was very helpful during my visit."})
        Review.objects.get_or_create(room=rooms[1], user=darshan, defaults={"rating": 4, "comment": "Good value and a convenient location for college."})
        self.stdout.write(self.style.SUCCESS("Demo data created. Login with sukruth / demo12345, darshan / demo12345, or demo_owner / demo12345."))
