from django.db import models
from django.conf import settings
from profiles.constants import BLOOD_GROUP_CHOICES

class BloodRequest(models.Model):
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    blood_group = blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES,
        null=True,
        blank=True
    )
    hospital_name = models.CharField(max_length=150)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

