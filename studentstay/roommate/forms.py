from django import forms
from .models import RoommatePost


class RoommatePostForm(forms.ModelForm):
    class Meta:
        model = RoommatePost
        fields = ["preferred_location", "budget", "has_room", "room_details", "move_in_date", "gender_preference", "bio", "is_active"]
        widgets = {
            "room_details": forms.Textarea(attrs={"rows": 4, "placeholder": "Example: Shared 2BHK, furnished room, Wi-Fi included, rent split ₹4,500."}),
            "move_in_date": forms.DateInput(attrs={"type": "date"}),
            "bio": forms.Textarea(attrs={"rows": 5, "placeholder": "Tell potential roommates about yourself and your preferences."}),
        }
