from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserAnswers
from .utils import evaluate_submission

@receiver(post_save, sender=UserAnswers)
def evaluate_user_submission(sender, instance, created, **kwargs):
    if created:
        evaluate_submission(instance)
