from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import UserProfile
from courses.models import Course, Enrollment
from quizzes.models import UserQuizResult


@login_required
def dashboard_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    enrollments = Enrollment.objects.filter(user=request.user).select_related("course")
    quiz_history = UserQuizResult.objects.filter(user=request.user).select_related("quiz").order_by("-completed_at")
    enrolled_course_ids = enrollments.values_list("course_id", flat=True)
    recommendations = Course.objects.filter(difficulty_level=profile.level).exclude(id__in=enrolled_course_ids)[:5]

    context = {
        "profile": profile,
        "enrollments": enrollments,
        "quiz_history": quiz_history,
        "recommendations": recommendations,
    }
    return render(request, "dashboard/index.html", context)
