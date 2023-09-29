# importing the receiver decorator
# from django.dispatch import receiver

from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from .models import Profile
from .task import send_email


# using the receiver decorator
# @receiver(post_save,sender=User)


def create_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile.objects.create(
            user=user, username=user.username, name=user.first_name, email=user.email
        )

        subject = "Welcome to DevSearch"
        message = f"We are glad you are here {profile.username}"

        send_email(subject, message, profile.email)


def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created != True:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


# @receiver(post_save,sender=User)


def delete_user(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(create_profile, sender=User)
post_save.connect(update_user, sender=Profile)
post_delete.connect(delete_user, sender=Profile)
