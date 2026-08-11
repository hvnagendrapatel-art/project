from django.contrib import admin
from .models import RoommatePost


@admin.register(RoommatePost)
class RoommatePostAdmin(admin.ModelAdmin):
    list_display = ("user", "preferred_location", "budget", "is_active", "created_at")
    list_filter = ("is_active", "gender_preference")
    search_fields = ("user__username", "preferred_location")
