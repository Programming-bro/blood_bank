from django.db import models
from django.conf import settings
from .constants import BLOOD_GROUP_CHOICES




class DonorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES,
        null=True,
        blank=True
    )
    age = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    last_donation_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_group}"