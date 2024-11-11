from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework.authtoken.models import Token
from image_cropping import ImageCropField, ImageRatioField
from .constants import USER_ROLE_CHOICES


class Member(AbstractUser):
    user_id =  models.CharField(max_length=15,primary_key=True, unique=True)
    username = models.CharField(max_length=32, null=False, blank=False, unique=True)
    password = models.CharField(max_length=256, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField("Phone", max_length=50, null=True, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=USER_ROLE_CHOICES, default='recruiter', blank=False, null=False)
    avatar = ImageCropField(
        ("Avatar"), blank=True, upload_to='avatars', null=True,
        default=r'static\\images\userIcon.png')
    cropping = ImageRatioField('avatar', '430x430')
    
    USERNAME_FIELD = "user_id"
    
    def __str__(self):
        return self.username + ' - ' + self.email
    
    def get_role(self):
        for k, v in USER_ROLE_CHOICES:
            if k == self.role:
                return v