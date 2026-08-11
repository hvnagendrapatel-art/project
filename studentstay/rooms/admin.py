from django.contrib import admin
from .models import Review, Room, RoomImage, Wishlist


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "room_type", "rent", "location", "is_available")
    list_filter = ("room_type", "is_available")
    search_fields = ("title", "location", "college_nearby")
    inlines = [RoomImageInline]


admin.site.register((RoomImage, Wishlist, Review))
