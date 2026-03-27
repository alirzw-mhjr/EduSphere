from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from quizzes.models import UserQuizResult


@login_required
def take_quiz_view(request, quiz_id):
    result = UserQuizResult.objects.filter(user=request.user, quiz_id=quiz_id).first()
    return render(request, "quizzes/take.html", {"quiz_id": quiz_id, "result": result})


@login_required
def quiz_result_view(request, quiz_id):
    result = get_object_or_404(UserQuizResult, user=request.user, quiz_id=quiz_id)
    feedback = "Great effort! Keep practicing."
    if result.score >= 76:
        feedback = "Excellent! You are performing at an advanced level."
    elif result.score >= 51:
        feedback = "Good work. You are progressing well."
    return render(request, "quizzes/result.html", {"result": result, "feedback": feedback})
