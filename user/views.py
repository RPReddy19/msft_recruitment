from django.shortcuts import render
# accounts/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer, LoginSerializer, UpdateUserSerializer
from .models import Member
# Signup View
class UserCreateView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    

     # Create a token for the new user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        user.is_active=True
        user.save()
        
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user": serializer.data,
            "message": "User created successfully.",
            "token": token.key
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
        token, created = Token.objects.get_or_create(user=member)


        return Response({
            "message": "Login successful",
            'token': token.key,
            "username": member.username,
            # You can add other user-related data if needed
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()  # Delete the token to log the user out
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)