from django import forms
from django.core.validators import MaxValueValidator
from django.forms import inlineformset_factory

from .models import Review, Room, RoomImage


class RoomForm(forms.ModelForm):
    rent = forms.IntegerField(
        validators=[MaxValueValidator(5999)],
        widget=forms.NumberInput(attrs={"min": 1, "max": 5999}),
    )
    shared_room_capacity = forms.ChoiceField(required=False, choices=[("", "Select share count"), (2, "2 people"), (3, "3 people"), (4, "4 people")], widget=forms.Select())
    shared_room_price_per_person = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Room
        fields = ["title", "description", "room_type", "rent", "shared_room_capacity", "shared_room_price_per_person", "location", "college_nearby", "distance_from_college", "is_available"]
        widgets = {"description": forms.Textarea(attrs={"rows": 5})}

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("room_type") == "shared":
            capacity = cleaned_data.get("shared_room_capacity")
            if not capacity:
                self.add_error("shared_room_capacity", "Select how many people will share this room.")
                return cleaned_data

            price_map = {2: 2500, 3: 1200, 4: 1000}
            price = price_map.get(int(capacity))
            if price is None:
                self.add_error("shared_room_capacity", "Choose 2, 3, or 4 people for a shared room.")
            else:
                cleaned_data["shared_room_price_per_person"] = price
        return cleaned_data


RoomImageFormSet = inlineformset_factory(Room, RoomImage, fields=("image",), extra=3, can_delete=True)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {"rating": forms.Select(choices=[(n, f"{n} star{'s' if n != 1 else ''}") for n in range(1, 6)]), "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Share your experience"})}
