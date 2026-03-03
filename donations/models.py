from django.db import models
from django.conf import settings
from requests.models import BloodRequest

class DonationResponse(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('donated', 'Donated'),
            ('canceled', 'Canceled'),
            ('pending', 'Pending')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
