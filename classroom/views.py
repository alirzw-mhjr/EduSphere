from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from courses.models import Lesson


@login_required
def virtual_classroom_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, "classroom/virtual.html", {"lesson": lesson})
