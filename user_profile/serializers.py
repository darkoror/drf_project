from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.models import User


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_email(self, value):
        if not value:
            return value
        return value.lower()


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirmed_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        new_password = data['new_password']
        confirmed_password = data['confirmed_password']
        if new_password != confirmed_password:
            raise serializers.ValidationError("The two password fields didn't match.")
        return data


class ChangePasswordSerializer(PasswordSerializer):
    """Serializer for password change endpoint."""
    old_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        if not self.instance.check_password(value):
            raise ValidationError("Wrong current password.")
        return value

    def update(self, instance, validated_data):
        self.instance.set_password(validated_data.get('new_password'))
        self.instance.save()
        return self.instance
