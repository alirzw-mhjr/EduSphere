from django.urls import path

from api import views

urlpatterns = [
    path("register/", views.register_api, name="api_register"),
    path("login/", views.login_api, name="api_login"),
    path("courses/", views.courses_api, name="api_courses"),
    path("courses/<int:pk>/", views.course_detail_api, name="api_course_detail"),
    path("enroll/", views.enroll_api, name="api_enroll"),
    path("quizzes/<int:pk>/", views.quiz_detail_api, name="api_quiz_detail"),
    path("quizzes/<int:pk>/submit/", views.submit_quiz_api, name="api_quiz_submit"),
    path("recommendations/", views.recommendations_api, name="api_recommendations"),
    path("chat/<int:lesson_id>/", views.chat_api, name="api_chat"),
]
