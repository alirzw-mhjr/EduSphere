from django.contrib import admin
from courses.models import Course, Enrollment, Lesson

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Enrollment)
