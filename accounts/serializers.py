# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Influencer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']

class InfluencerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Influencer
        fields = '__all__'

# class BrandSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = Brand
#         fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
        )
        return user
