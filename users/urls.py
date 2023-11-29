"""Specify urls for users app"""
from rest_framework_simplejwt import views as jwt_views
from django.urls import path
from users.views import RegistrationView, LoginView, ChangePasswordView, UserListView

app_name = 'users'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='register'),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user_list'),
]
