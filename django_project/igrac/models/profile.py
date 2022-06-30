"""Extended IGRAC specific profile."""

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class IgracProfile(models.Model):
    """Extended IGRAC specific profile."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    join_reason = models.TextField(max_length=500, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        IgracProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance: User, **kwargs):
    try:
        instance.igracprofile.save()
    except IgracProfile.DoesNotExist:
        IgracProfile.objects.create(user=instance)
