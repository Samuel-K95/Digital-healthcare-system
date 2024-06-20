from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, Doctor



@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender,instance,created,**kwargs):
    print(created)
    if created:
        Doctor.objects.create(user=instance)
        
        print('Doctor account has been created')
    else:
        try:
            profile = Doctor.objects.get(user=instance)
            profile.save()
        except:
            print("Doctor account doesn't!")
        print('User is updated!')


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, " is being saved.")

