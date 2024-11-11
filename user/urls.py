# accounts/urls.py
from django.urls import path
from .views import UserCreateView, LoginView, MemberUpdateView, LogoutView
from rest_framework_simplejwt.views import TokenBlacklistView


urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update/<str:username>/', MemberUpdateView.as_view(), name='member-update'),
]