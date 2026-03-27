from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.forms import RegisterForm
from accounts.models import UserProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Registration successful.")
        return redirect("dashboard:index")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, "accounts/profile.html", {"profile": profile})
