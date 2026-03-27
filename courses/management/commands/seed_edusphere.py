from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from courses.models import Course, Lesson
from quizzes.models import Question, Quiz


class Command(BaseCommand):
    help = "Populate sample courses, lessons, and quizzes for EduSphere"

    def handle(self, *args, **options):
        instructor, _ = User.objects.get_or_create(
            username="instructor",
            defaults={"email": "instructor@example.com"},
        )
        if not instructor.has_usable_password():
            instructor.set_password("instructor123")
            instructor.save()

        course_data = [
            {
                "title": "Python Basics",
                "description": "Learn Python fundamentals, syntax, and problem-solving.",
                "difficulty_level": "beginner",
                "lessons": [
                    {
                        "title": "Variables and Data Types",
                        "content": "This lesson introduces variables, strings, integers, and floats.",
                        "video_url": "https://www.youtube.com/embed/rfscVS0vtbw",
                        "quiz": [
                            ("Which keyword is used to create a function?", "def", "func", "lambda", "make", "A"),
                            ("What is the type of 3.14?", "int", "float", "str", "bool", "B"),
                        ],
                    },
                    {
                        "title": "Conditions and Loops",
                        "content": "Understand if statements, for loops, and while loops.",
                        "video_url": "https://www.youtube.com/embed/kqtD5dpn9C8",
                        "quiz": [
                            ("Which loop iterates over a sequence?", "if", "for", "when", "switch", "B"),
                            ("What does break do?", "Skips to next loop", "Ends loop", "Repeats loop", "Defines loop", "B"),
                        ],
                    },
                ],
            },
            {
                "title": "Web APIs with DRF",
                "description": "Build RESTful APIs using Django REST Framework.",
                "difficulty_level": "intermediate",
                "lessons": [
                    {
                        "title": "Serializers and Views",
                        "content": "Use serializers and API views to expose models.",
                        "video_url": "https://www.youtube.com/embed/tu98QnVCQdE",
                        "quiz": [
                            ("DRF serializer converts model to?", "XML", "JSON-like data", "CSV", "HTML only", "B"),
                            ("APIView is from?", "django.views", "rest_framework.views", "requests", "sqlite3", "B"),
                        ],
                    }
                ],
            },
            {
                "title": "Machine Learning Essentials",
                "description": "Explore supervised learning concepts and model evaluation.",
                "difficulty_level": "advanced",
                "lessons": [
                    {
                        "title": "Model Evaluation",
                        "content": "Understand precision, recall, and confusion matrix.",
                        "video_url": "https://www.youtube.com/embed/0Lt9w-BxKFQ",
                        "quiz": [
                            ("Precision is:", "TP/(TP+FP)", "TP/(TP+FN)", "TN/(TN+FP)", "FP/(TP+TN)", "A"),
                            ("Recall is:", "TP/(TP+FN)", "TP/(TP+FP)", "TN/(TN+FN)", "FN/(TP+FP)", "A"),
                        ],
                    }
                ],
            },
        ]

        for item in course_data:
            course, _ = Course.objects.get_or_create(
                title=item["title"],
                defaults={
                    "description": item["description"],
                    "difficulty_level": item["difficulty_level"],
                    "created_by": instructor,
                },
            )
            for index, lesson_data in enumerate(item["lessons"], start=1):
                lesson, _ = Lesson.objects.get_or_create(
                    course=course,
                    title=lesson_data["title"],
                    defaults={
                        "content": lesson_data["content"],
                        "video_url": lesson_data["video_url"],
                        "order": index,
                    },
                )
                quiz, _ = Quiz.objects.get_or_create(
                    lesson=lesson,
                    defaults={"title": f"{lesson.title} Quiz", "max_score": 100},
                )
                for q in lesson_data["quiz"]:
                    Question.objects.get_or_create(
                        quiz=quiz,
                        text=q[0],
                        defaults={
                            "option_a": q[1],
                            "option_b": q[2],
                            "option_c": q[3],
                            "option_d": q[4],
                            "correct_answer": q[5],
                        },
                    )

        self.stdout.write(self.style.SUCCESS("Sample EduSphere data created successfully."))
