from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("StayFinder profile", {"fields": ("phone", "college", "profile_picture", "role")}),)
    list_display = ("username", "email", "role", "college", "is_staff")
