from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from roommate.models import RoommatePost
from rooms.models import Wishlist


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_rooms"] = self.request.user.rooms.prefetch_related("images")
        context["my_roommate_posts"] = RoommatePost.objects.filter(user=self.request.user)
        context["wishlist"] = Wishlist.objects.filter(user=self.request.user).select_related("room").prefetch_related("room__images")
        return context
