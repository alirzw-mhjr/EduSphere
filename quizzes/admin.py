from django.contrib import admin
from quizzes.models import Question, Quiz, UserQuizResult

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(UserQuizResult)
