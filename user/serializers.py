from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password

import re
from .models import Member

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Member
        fields = ("user_id", "username", "password", "email", "first_name", "last_name", "phone", "role")
        
    def create(self, validated_data):
        member = Member(
            username=validated_data['username'],
        )
        if self.validate_password(validated_data['password']):
            validated_data['password'] = make_password(validated_data['password'])
            validated_data['avatar'] = None
            return super().create(validated_data)
    
    def validate_password(self, value):
        # Define password requirements
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[@$!%*?&]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value
    
    def update(self, instance, validated_data):
        # Update the username if provided
        instance.username = validated_data.get('username', instance.username)

        # Update the password if provided and hash it
        if 'password' in validated_data:
            validated_data["password"] = make_password(validated_data['password'])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class UpdateUserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, required=False)
    # email = serializers.EmailField(required=False)
    # first_name = serializers.CharField(max_length=150, required=False)
    # last_name = serializers.CharField(max_length=150, required=False)
    # phone = serializers.CharField(max_length=50, required=False)
    class Meta:
            model = Member
            fields = ("password", "email", "first_name", "last_name", "phone")
            extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'password': {'required': False},
            'phone': {'required': False},
        }

    def update(self, instance, validated_data):
        # Update the username if provided
        instance.username = validated_data.get('username', instance.username)

        if 'password' in validated_data:
            validated_data["password"] = make_password(validated_data['password'])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            member = Member.objects.get(username=data['username'])
        except Member.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password.")

        if not check_password(data['password'], member.password):
            raise serializers.ValidationError("Invalid username or password.")

        return member