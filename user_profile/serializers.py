from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from authentication.models import User


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            error = f"User with the email '{value}' already exists"
            raise serializers.ValidationError(error)
        return value.lower()

    # def update(self, instance, validated_data):
    #     instance.email = validated_data['email']
    #     instance.username = validated_data['username']
    #     instance.save()
    #
    #     return instance


class ChangePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("password",)
        write_only_fields = ("password",)
