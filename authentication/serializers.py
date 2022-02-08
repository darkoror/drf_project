from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from authentication import constants
from authentication.models import User


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    default_error_messages = {
        'password': constants.PASSWORDS_DID_NOT_MATCH,
    }

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "password_confirm", "avatar")
        read_only_fields = ("id",)

    def validate_email(self, value):
        return value.lower()

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            self.fail('password')

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user


class ActivateUserSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    default_error_messages = {
        "invalid": constants.INVALID_TOKEN_ERROR,
        "user_activated": constants.USER_ALREADY_ACTIVATED_ERROR,
    }

    def validate(self, data):
        token = data['token']
        try:
            uid, token = token.split('.')
            uid = int(force_str(urlsafe_base64_decode(uid)))
        except (TypeError, ValueError):
            self.fail("invalid")

        try:
            self.user = User.objects.get(id=uid)
        except User.DoesNotExist:
            self.fail("invalid")

        if not default_token_generator.check_token(self.user, token):
            self.fail("invalid")

        if self.user.is_active:
            self.fail("user_activated")

        data['id'] = uid
        return data

    def activate_user(self):
        """if token is valid then activate the user, after that user can log in"""
        self.user.is_active = True
        self.user.save()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    default_error_messages = {
        "invalid_email": constants.INVALID_EMAIL_ERROR,
    }

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            return email
        self.fail("invalid_email")


class PasswordResetCompleteSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    default_error_messages = {
        "invalid": constants.INVALID_TOKEN_ERROR,
        "password": constants.PASSWORDS_DID_NOT_MATCH,
    }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            self.fail('password')

        return attrs

    def validate_token(self, value):
        try:
            uid, token = value.split('.')
            uid = int(force_str(urlsafe_base64_decode(uid)))
        except (TypeError, ValueError):
            self.fail("invalid")

        try:
            self.user = User.objects.get(id=uid)
        except User.DoesNotExist:
            self.fail("invalid")

        if not default_token_generator.check_token(self.user, token):
            self.fail("invalid")

        return value

    def set_new_password(self):
        self.user.set_password(self.validated_data['password'])
        self.user.save()
