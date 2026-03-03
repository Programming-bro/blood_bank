from rest_framework import serializers
from .models import BloodRequest
from users.serializers import UserSerializer


class BloodRequestSerializer(serializers.ModelSerializer):
    requester = UserSerializer(read_only=True)
    class Meta:
        model = BloodRequest
        fields = [
            'id',
            'requester',
            'patient_name',
            'blood_group',
            'hospital_name',
            'address',
            'created_at',
            'is_active'
        ]
        read_only_fields = ['created_at']