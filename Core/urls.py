from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")
    return redirect("courses:list")

urlpatterns = [
    path("", home_redirect, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("courses/", include("courses.urls")),
    path("quizzes/", include("quizzes.urls")),
    path("classroom/", include("classroom.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("api/", include("api.urls")),
]
