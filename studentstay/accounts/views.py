from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import OwnerSignUpForm, SignUpForm
from .models import CustomUser


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        initial = {}
        if request.GET.get("role") in dict(CustomUser.ROLE_CHOICES):
            initial["role"] = request.GET["role"]
        form = SignUpForm(initial=initial)

    return render(
        request,
        "accounts/signup.html",
        {"form": form}
    )


def owner_signup_view(request):
    if request.method == "POST":
        form = OwnerSignUpForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            messages.success(request, "Your owner account is ready. You can now list your first property.")
            return redirect("owner-portal")
    else:
        form = OwnerSignUpForm()
    return render(request, "accounts/owner_signup.html", {"form": form})


def owner_login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role == "owner":
                login(request, user)
                return redirect("owner-portal")
            messages.error(request, "This is a student account. Please use the regular login page.")
    else:
        form = AuthenticationForm(request)
    return render(request, "accounts/owner_login.html", {"form": form})
