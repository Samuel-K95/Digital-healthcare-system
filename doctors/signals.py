from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Doctor


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        # Only auto-create a Doctor profile for users explicitly marked as staff
        if getattr(instance, 'is_staff', False):
            Doctor.objects.create(user=instance)
            print('Doctor account has been created for staff user')
    else:
        try:
            profile = Doctor.objects.get(user=instance)
            profile.save()
        except Doctor.DoesNotExist:
            pass


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    # No-op logging hook kept for development
    return

