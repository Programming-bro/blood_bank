from rest_framework import serializers
from .models import DonationResponse
from users.serializers import UserSerializer
from requests.serializers import BloodRequestSerializer


class DonationResponseSerializer(serializers.ModelSerializer):
    donor = UserSerializer(read_only=True)
    request = BloodRequestSerializer(read_only=True)

    class Meta:
        model = DonationResponse
        fields = [
            'id',
            'donor',
            'request',
            'status',
            'created_at'
        ]