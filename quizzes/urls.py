from django.urls import path

from quizzes import views

app_name = "quizzes"

urlpatterns = [
    path("<int:quiz_id>/take/", views.take_quiz_view, name="take"),
    path("<int:quiz_id>/result/", views.quiz_result_view, name="result"),
]
