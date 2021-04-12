from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView

from authentication.serializers import SignUpSerializer, EmailVerifySerializer, PasswordResetSerializer, \
    SetNewPasswordSerializer
from authentication.models import User
from authentication.tasks import send_email
from drf_project.settings import FRONT_END_DOMAIN, FRONT_END_ACTIVATE_EMAIL_LINK


class SignUpView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def perform_create(self, serializer):
        serializer.save()
        user = User.objects.get(email=serializer.data["email"])

        token = f"{urlsafe_base64_encode(force_bytes(user.email))}.{default_token_generator.make_token(user)}"

        if FRONT_END_DOMAIN:
            absurl = f"{FRONT_END_DOMAIN}{FRONT_END_ACTIVATE_EMAIL_LINK}?token={token}"
        else:
            current_site = get_current_site(self.request).domain
            relativeLink = reverse("email-verify")
            absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)

        body = "Hi " + user.username + "\nUse link below to verify your email \n" + absurl
        subject = "Verify your email"

        send_email.delay(subject, body, [user.email])


class EmailVerify(APIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate_user()
        return Response({"email": "Successfully activated"}, status=status.HTTP_200_OK)


class PasswordReset(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_email()
        return Response({"password": "Password reset link sent to your email"}, status=status.HTTP_200_OK)


class SetNewPassword(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SetNewPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response({"password": "Successfully reset"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
