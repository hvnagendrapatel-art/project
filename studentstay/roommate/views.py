from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import RoommatePostForm
from .models import RoommatePost


class RoommateListView(ListView):
    model = RoommatePost
    template_name = "roommate/roommate_list.html"
    context_object_name = "posts"
    paginate_by = 12

    def get_queryset(self):
        posts = RoommatePost.objects.filter(is_active=True).select_related("user")
        if q := self.request.GET.get("q", "").strip():
            posts = posts.filter(Q(preferred_location__icontains=q) | Q(user__college__icontains=q))
        if budget := self.request.GET.get("max_budget"):
            if budget.isdigit():
                posts = posts.filter(budget__lte=budget)
        return posts


class RoommateDetailView(DetailView):
    model = RoommatePost
    template_name = "roommate/roommate_detail.html"


class PostOwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.get_object().user == self.request.user


class RoommateCreateView(LoginRequiredMixin, CreateView):
    model = RoommatePost
    form_class = RoommatePostForm
    template_name = "roommate/roommate_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RoommateUpdateView(PostOwnerRequiredMixin, UpdateView):
    model = RoommatePost
    form_class = RoommatePostForm
    template_name = "roommate/roommate_form.html"


class RoommateDeleteView(PostOwnerRequiredMixin, DeleteView):
    model = RoommatePost
    template_name = "roommate/roommate_confirm_delete.html"
    success_url = reverse_lazy("roommate-list")
