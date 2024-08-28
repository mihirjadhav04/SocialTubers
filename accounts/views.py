# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import Influencer
from .serializers import (
    UserSerializer, InfluencerSerializer, 
    UserRegistrationSerializer
)

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "success": True,
            "message": "User registered successfully!",
            "data": {
                "user": UserSerializer(user).data,
                "token": token.key
            },
            "status_code": status.HTTP_201_CREATED
        }, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "success": True,
                "message": "Logged In Successfully!",
                "data": {
                    "token": token.key,
                    "user": UserSerializer(user).data
                },
                "status_code": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Invalid credentials. Please check your email and password.",
            "errors": {
                "email": ["Ensure this field is correct."],
                "password": ["Ensure this field is correct."]
            },
            "status_code": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get the user's token
        token = Token.objects.get(user=request.user)
        # Delete the token to logout the user
        token.delete()
        
        return Response({
            "success": True,
            "message": "Logged out successfully!",
            "status_code": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

class InfluencerListView(generics.ListAPIView):
    queryset = Influencer.objects.all()
    serializer_class = InfluencerSerializer

# class BrandListView(generics.ListAPIView):
#     queryset = Brand.objects.all()
#     serializer_class = BrandSerializer
