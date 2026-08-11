from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ReviewForm, RoomForm, RoomImageFormSet
from .models import Review, Room, Wishlist


def home(request):
    rooms = Room.objects.filter(is_available=True).prefetch_related("images")[:3]
    return render(request, "rooms/home.html", {"featured_rooms": rooms, "room_count": Room.objects.filter(is_available=True).count()})


def owner_portal(request):
    listings = Room.objects.none()
    if request.user.is_authenticated and request.user.role == "owner":
        listings = request.user.rooms.prefetch_related("images")
    return render(request, "rooms/owner_portal.html", {"listings": listings})


class RoomListView(ListView):
    model = Room
    template_name = "rooms/room_list.html"
    context_object_name = "rooms"
    paginate_by = 12

    def get_queryset(self):
        rooms = Room.objects.filter(is_available=True).prefetch_related("images")
        q = self.request.GET.get("q", "").strip()
        if q:
            rooms = rooms.filter(Q(location__icontains=q) | Q(college_nearby__icontains=q) | Q(title__icontains=q))
        if room_type := self.request.GET.get("room_type"):
            rooms = rooms.filter(room_type=room_type)
        if max_rent := self.request.GET.get("max_rent"):
            if max_rent.isdigit():
                rooms = rooms.filter(rent__lte=max_rent)
        return rooms


class RoomDetailView(DetailView):
    model = Room
    template_name = "rooms/room_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_form"] = ReviewForm()
        context["is_saved"] = self.request.user.is_authenticated and Wishlist.objects.filter(user=self.request.user, room=self.object).exists()
        return context


class RoomOwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.get_object().owner == self.request.user


class PropertyOwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Only accounts registered as property owners can publish rental listings."""

    def test_func(self):
        return self.request.user.role == "owner"

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.info(self.request, "Register as a Property Owner to list a room for rent.")
            return redirect("room-list")
        return super().handle_no_permission()


class RoomFormsetMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "formset" not in context:
            context["formset"] = RoomImageFormSet(self.request.POST or None, self.request.FILES or None, instance=getattr(self, "object", None))
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        if formset.is_valid():
            self.object = form.save(commit=False)
            if not self.object.pk:
                self.object.owner = self.request.user
            self.object.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.object.get_absolute_url())
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class RoomCreateView(PropertyOwnerRequiredMixin, RoomFormsetMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = "rooms/room_form.html"


class RoomUpdateView(RoomOwnerRequiredMixin, RoomFormsetMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = "rooms/room_form.html"


class RoomDeleteView(RoomOwnerRequiredMixin, DeleteView):
    model = Room
    template_name = "rooms/room_confirm_delete.html"
    success_url = reverse_lazy("room-list")


@login_required
@require_POST
def toggle_wishlist(request, pk):
    room = get_object_or_404(Room, pk=pk)
    item, created = Wishlist.objects.get_or_create(user=request.user, room=room)
    if created:
        messages.success(request, "Room saved to your wishlist.")
    else:
        item.delete()
        messages.info(request, "Room removed from your wishlist.")
    return redirect("room-detail", pk=pk)


@login_required
@require_POST
def toggle_rental_status(request, pk):
    room = get_object_or_404(Room, pk=pk, owner=request.user)
    room.is_available = not room.is_available
    room.save(update_fields=["is_available"])
    messages.success(request, f"{room.title} is now {'available for rent' if room.is_available else 'off rent'}.")
    return redirect(request.POST.get("next") or "dashboard")


@login_required
@require_POST
def create_review(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if room.owner == request.user:
        return HttpResponseForbidden("You cannot review your own listing.")
    form = ReviewForm(request.POST)
    if form.is_valid():
        Review.objects.update_or_create(room=room, user=request.user, defaults=form.cleaned_data)
        messages.success(request, "Your review has been saved.")
    else:
        messages.error(request, "Please provide a rating and comment.")
    return redirect("room-detail", pk=pk)
