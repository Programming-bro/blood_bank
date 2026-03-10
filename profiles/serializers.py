from rest_framework import serializers
from .models import DonorProfile
from users.serializers import UserSerializer
from donations.models import DonationResponse
from donations.serializers import DonationResponseSerializer


class DonorListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    name = serializers.CharField(source='user.username')

    class Meta:
        model = DonorProfile
        fields = [
            'id',
            'name',
            'blood_group',
            'last_donation_date',
            'address',  
        ]

class DonorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    donation_history = serializers.SerializerMethodField()

    class Meta:
        model = DonorProfile
        fields = [
            'id',
            'user',
            'age',
            'address',
            'last_donation_date',
            'is_available',
            'is_premium',
            'blood_group',
            'donation_history'
        ]

    def get_donation_history(self, obj):
        donations = DonationResponse.objects.filter(donor=obj.user)
        return DonationResponseSerializer(donations, many=True).data
    
    def update(self, instance, validated_data):
        
        user_data = validated_data.pop('user', {})
        blood_group = user_data.get('blood_group')

        if blood_group:
            instance.user.blood_group = blood_group
            instance.user.save()

        return super().update(instance, validated_data)