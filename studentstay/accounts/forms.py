from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "phone",
            "college",
            "role",
            "password1",
            "password2",
        ]


class OwnerSignUpForm(UserCreationForm):
    """A short registration form used exclusively by property owners."""

    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "owner"
        if commit:
            user.save()
        return user
