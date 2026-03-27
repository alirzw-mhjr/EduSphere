from django.contrib.auth.models import User
from django.db import models

from courses.models import Lesson


class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, related_name="quiz", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    max_score = models.IntegerField(default=100)

    def __str__(self):
        return self.title


class Question(models.Model):
    ANSWER_CHOICES = [("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")]

    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200, blank=True, null=True)
    option_d = models.CharField(max_length=200, blank=True, null=True)
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)

    def __str__(self):
        return self.text[:50]


class UserQuizResult(models.Model):
    user = models.ForeignKey(User, related_name="quiz_results", on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name="results", on_delete=models.CASCADE)
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "quiz"]

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}: {self.score}"

# Create your models here.
