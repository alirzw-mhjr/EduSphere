from django.urls import path

from classroom import views

app_name = "classroom"

urlpatterns = [
    path("<int:lesson_id>/", views.virtual_classroom_view, name="virtual"),
]
