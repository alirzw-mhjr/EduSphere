from django.urls import path

from courses import views

app_name = "courses"

urlpatterns = [
    path("", views.course_list_view, name="list"),
    path("<int:course_id>/", views.course_detail_view, name="detail"),
    path("<int:course_id>/enroll/", views.enroll_view, name="enroll"),
    path("lesson/<int:lesson_id>/", views.lesson_view, name="lesson"),
]
