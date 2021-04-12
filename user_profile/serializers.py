from rest_framework import serializers

from authentication.models import User


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_email(self, value):
        if not value:
            return value
        return value.lower()


class ChangePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("password",)
        write_only_fields = ("password",)
