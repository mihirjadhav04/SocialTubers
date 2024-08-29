# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Influencer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']

class InfluencerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Influencer
        fields = ['channel_name', 'youtube_id', 'instagram_id', 'created_date']

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
