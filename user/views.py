from django.shortcuts import render
# accounts/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer
from .serializers import UserSerializer, LoginSerializer, UpdateUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Member
# Signup View
class UserCreateView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": serializer.data,
            "message": "User created successfully."
        }, status=status.HTTP_201_CREATED)

class MemberUpdateView(generics.UpdateAPIView):
    queryset = Member.objects.all()
    serializer_class = UpdateUserSerializer
    lookup_field = 'username'  # You can use username as a unique identifier
    permission_classes = [IsAuthenticated]

    def patch(self, request, username, *args, **kwargs):
        member = self.get_object()  # Get the member instance by username
        serializer = self.get_serializer(member, data=request.data, partial=True)  # Allow partial updates
        serializer.is_valid(raise_exception=True)  # Validate the data
        serializer.save()  # Save the updated instance
        return Response(serializer.data, status=status.HTTP_200_OK)

# Custom Token Serializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token

# Login View
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.validated_data  # The validated member object
        token = CustomTokenObtainPairSerializer.get_token(member)
        return Response({
            "message": "Login successful",
            "username": member.username,
            # You can add other user-related data if needed
            "token": str(token.access_token),
            "refresh_token": str(token)
        }, status=status.HTTP_200_OK)

class LogoutView(generics.CreateAPIView):
    serializer_class = TokenBlacklistSerializer

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")  # get refresh token from request body
            token = RefreshToken(refresh_token)
            token.blacklist()  # blacklist the refresh token
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(str(e))
            return Response({'error': str(e)},status=status.HTTP_400_BAD_REQUEST)