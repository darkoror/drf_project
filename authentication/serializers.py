from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

from authentication.models import User
from authentication.tasks import send_email
from drf_project.settings import FRONT_END_DOMAIN, FRONT_END_PASSWORD_RESET_LINK


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        read_only_fields = ("id",)
        write_only_fields = ("password",)

    def validate_email(self, value):
        return value.lower()

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user


class EmailVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        token = data['token']
        error = f"Provided activation token '{token}' is not valid"
        try:
            uid, token = token.split('.')
            uid = force_text(urlsafe_base64_decode(uid))
        except (TypeError, ValueError):
            raise serializers.ValidationError(error)

        try:
            user = User.objects.get(email=uid)
        except User.DoesNotExist:
            raise serializers.ValidationError(error)

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError(error)

        data['email'] = uid
        return data

    def activate_user(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.is_active = True
        user.save()


class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("id", "email")
        read_only_fields = ("id",)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            return value.lower()
        else:
            raise serializers.ValidationError(f"There is no such user with provided email '{value}'")

    def send_email(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.save()

        token = f"{urlsafe_base64_encode(force_bytes(user.email))}.{default_token_generator.make_token(user)}"

        if FRONT_END_DOMAIN:
            absurl = f"{FRONT_END_DOMAIN}{FRONT_END_PASSWORD_RESET_LINK}?token={token}"
        else:
            current_site = get_current_site(self.context["request"]).domain
            relativeLink = reverse("email-verify")
            absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)

        body = "Hi " + user.username + "\nUse link below to reset your password \n" + absurl
        subject = "Reset password"

        send_email.delay(subject, body, [user.email])


class SetNewPasswordSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, required=True)
    password_repeat = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("id", "password", "password_repeat", "token")
        read_only_fields = ("id",)
        write_only_fields = ("password", "password_repeat")

    def validate(self, data):
        token = data['token']
        error = f"Provided activation token '{token}' is not valid"
        try:
            uid, token = token.split('.')
            uid = force_text(urlsafe_base64_decode(uid))
        except (TypeError, ValueError):
            raise serializers.ValidationError(error)

        try:
            user = User.objects.get(email=uid)
        except User.DoesNotExist:
            raise serializers.ValidationError(error)

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError(error)

        data['email'] = uid
        return data

    def validate_password(self, value):
        validate_password(value)
        if value != self.initial_data["password_repeat"]:
            raise serializers.ValidationError("Passwords don`t match")
        return value

    def set_new_password(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['password'])
        user.save()
