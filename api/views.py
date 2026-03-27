from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.models import UserProfile
from api.serializers import (
    ChatMessageSerializer,
    CourseSerializer,
    QuizDetailSerializer,
    RegisterSerializer,
)
from classroom.models import ChatMessage
from courses.models import Course, Enrollment, Lesson
from quizzes.models import Quiz, UserQuizResult


@api_view(["POST"])
@permission_classes([AllowAny])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"message": "User registered", "token": token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)
    if not user:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    login(request, user)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"message": "Login successful", "token": token.key}, status=status.HTTP_200_OK)


@api_view(["GET"])
def courses_api(request):
    queryset = Course.objects.all().order_by("-created_at")
    serializer = CourseSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def course_detail_api(request, pk):
    course = get_object_or_404(Course, id=pk)
    serializer = CourseSerializer(course)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def enroll_api(request):
    course_id = request.data.get("course_id")
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        return Response({"message": "Enrolled successfully"}, status=status.HTTP_201_CREATED)
    return Response({"message": "Already enrolled"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def quiz_detail_api(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)
    serializer = QuizDetailSerializer(quiz)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_quiz_api(request, pk):
    quiz = get_object_or_404(Quiz, id=pk)
    submitted_answers = request.data.get("answers", {})

    questions = quiz.questions.all()
    total_questions = questions.count()
    if total_questions == 0:
        return Response({"error": "Quiz has no questions"}, status=status.HTTP_400_BAD_REQUEST)

    correct_count = 0
    for question in questions:
        submitted = submitted_answers.get(str(question.id))
        if submitted == question.correct_answer:
            correct_count += 1

    score = round((correct_count / total_questions) * 100, 2)
    UserQuizResult.objects.update_or_create(
        user=request.user,
        quiz=quiz,
        defaults={"score": score},
    )

    if score <= 50:
        feedback = "You are currently at beginner level. Review lesson fundamentals."
    elif score <= 75:
        feedback = "Good work. You are progressing at intermediate level."
    else:
        feedback = "Excellent performance. Advanced level achieved."

    return Response(
        {
            "quiz_id": quiz.id,
            "score": score,
            "feedback": feedback,
            "correct_answers": correct_count,
            "total_questions": total_questions,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recommendations_api(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    enrolled = Enrollment.objects.filter(user=request.user).values_list("course_id", flat=True)
    recommendations = Course.objects.filter(difficulty_level=profile.level).exclude(id__in=enrolled)[:5]
    serializer = CourseSerializer(recommendations, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def chat_api(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == "GET":
        messages = ChatMessage.objects.filter(lesson=lesson).select_related("user")
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    text = request.data.get("message", "").strip()
    if not text:
        return Response({"error": "Message cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

    chat = ChatMessage.objects.create(user=request.user, lesson=lesson, message=text)
    serializer = ChatMessageSerializer(chat)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
