from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import UserProfile
from quizzes.models import UserQuizResult


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=UserQuizResult)
def update_profile_after_quiz(sender, instance, **kwargs):
    user = instance.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    results = UserQuizResult.objects.filter(user=user)
    average_score = results.aggregate(avg=Avg("score"))["avg"] or 0
    quizzes_taken = results.count()

    if average_score <= 50:
        level = "beginner"
    elif average_score <= 75:
        level = "intermediate"
    else:
        level = "advanced"

    profile.total_score = round(average_score, 2)
    profile.quizzes_taken = quizzes_taken
    profile.level = level
    profile.save(update_fields=["total_score", "quizzes_taken", "level", "last_activity"])
