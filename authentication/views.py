from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication import tasks
from authentication.serializers import SignUpSerializer, ActivateUserSerializer, PasswordResetSerializer, \
    PasswordResetCompleteSerializer
from authentication.utils import build_url
from drf_project.settings import ACTIVATION_PATH, PASSWORD_RESET_PATH
from authentication.models import User


class SignUpView(generics.CreateAPIView):
    """
    post:
    Create new user

    Register a user with obtained params
    """
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        context = {
            'link': build_url(scheme=self.request.scheme,
                              uid=urlsafe_base64_encode(force_bytes(user.id)),
                              token=default_token_generator.make_token(user),
                              path=ACTIVATION_PATH)
        }
        tasks.send_email.delay(subject="email/activate_account_subject.txt", template="email/activate_account.html",
                               emails=[user.email], context=context)


class ActivateUserView(APIView):
    """
    post:
    Activate user

    Activate a user by token
    """
    permission_classes = (AllowAny,)
    serializer_class = ActivateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.activate_user()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetView(APIView):
    """
    post:
    Password reset

    Send password reset link to email
    """
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data["email"])
        context = {
            'link': build_url(scheme=self.request.scheme,
                              uid=urlsafe_base64_encode(force_bytes(user.id)),
                              token=default_token_generator.make_token(user),
                              path=PASSWORD_RESET_PATH)
            }
        tasks.send_email.delay(subject="email/reset_password_subject.txt", template="email/reset_password.html",
                               emails=[user.email], context=context)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetCompleteView(APIView):
    """
    Password reset complete

    Reset password by token
    """
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetCompleteSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response(status=status.HTTP_204_NO_CONTENT)
