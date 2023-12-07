"""Define API views for users app"""
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.utils import get_tokens_for_user
from users.serializers import RegistrationSerializer, PasswordChangeSerializer, LeluUserSerializer
from users.serializers import WebsiteUserSerializer
from users.models import WebsiteUser, LeluUser
from users.website_user_authentication import WebsiteUserTokenAuthentication


class RegistrationView(APIView):
    """API for registering users"""
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """API for loging users"""
    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'},
                            status=status.HTTP_400_BAD_REQUEST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data},
                            status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'},
                        status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(APIView):
    """API to change password for LeluUser"""
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request},
                                              data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserListView(APIView):
    """API for getting info about authenticated user"""

    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        serializer = LeluUserSerializer(request.user)
        return Response(serializer.data)

class WebsiteUserListView(APIView):
    """API for WebsiteUser model"""

    def post(self, request):
        serializer = WebsiteUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoteAuthentication(APIView):
    """API to check Authorization token for authentication"""
    authentication_classes = [JWTAuthentication, WebsiteUserTokenAuthentication]

    def get(self, request):
        if isinstance(request.user, LeluUser):
            serializer = LeluUserSerializer(request.user)
            return Response(serializer.data)
        if isinstance(request.user, WebsiteUser):
            serializer = WebsiteUserSerializer(request.user)
            return Response(serializer.data)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
