from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username','email', 'password', 'first_name',
                  'last_name']
        
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer):
        ref_name = 'CustomUser'
        model = User
        fields = ['id', 'username', 'email']