from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile

from .utils import devsearch_email, account_varification_email

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            name=user.first_name + " " + user.last_name,
            email=user.email,
            username=user.username,           
        )
        profile.save()

        account_varification_email(str(profile.id), profile.email)


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()
