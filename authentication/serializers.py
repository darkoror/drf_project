from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from authentication.models import User


class SignUpSerializer(serializers.ModelSerializer):
    password_repeated = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "password_repeated", "role")
        read_only_fields = ("id", "role")
        write_only_fields = ("password", "password_repeated")

    def validate(self, data):
        if data["password_repeated"] != data["password"]:
            error = "Repeated password is not equal to password"
            raise serializers.ValidationError(error)
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            error = f"User with the email '{value}' already exists"
            raise serializers.ValidationError(error)
        return value.lower()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']

        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
