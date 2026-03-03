from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import DonorProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_donor_profile(sender, instance, created, **kwargs):
    if created:
        DonorProfile.objects.create(user=instance)