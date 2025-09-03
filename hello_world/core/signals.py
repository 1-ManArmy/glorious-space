# 👑 Django Signals - Royal Kingdom Events
# Signals for our magnificent platform events

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserActivity, Notification

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_activity(sender, instance, created, **kwargs):
    """Create user activity tracking when a new royal subject joins"""
    if created:
        UserActivity.objects.get_or_create(user=instance)
        
        # Welcome notification for new users
        Notification.objects.create(
            user=instance,
            title="👑 Welcome to the Royal Kingdom!",
            message="Your magnificent journey begins here. Explore, create, and build together!",
            notification_type='system'
        )
