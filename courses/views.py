from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course, Enrollment, Lesson


def course_list_view(request):
    level = request.GET.get("level")
    courses = Course.objects.all().order_by("-created_at")
    if level:
        courses = courses.filter(difficulty_level=level)
    return render(request, "courses/list.html", {"courses": courses, "selected_level": level})


def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    return render(request, "courses/detail.html", {"course": course, "is_enrolled": is_enrolled})


@login_required
def enroll_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    messages.success(request, f"You are now enrolled in {course.title}.")
    return redirect("courses:detail", course_id=course.id)


@login_required
def lesson_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    Enrollment.objects.get_or_create(user=request.user, course=lesson.course)
    quiz = getattr(lesson, "quiz", None)
    return render(request, "courses/lesson.html", {"lesson": lesson, "quiz": quiz})
