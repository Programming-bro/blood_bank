from django.contrib import admin
from donations.models import DonationResponse
from requests.models import BloodRequest
from profiles.models import DonorProfile
from users.models import User
# Register your models here.

admin.site.register(DonationResponse)
admin.site.register(BloodRequest)
admin.site.register(DonorProfile)
admin.site.register(User)