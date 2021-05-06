from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from authentication.models import User
from user_profile import constants


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')
        read_only_fields = ('id', 'email')


class PasswordChangeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    default_error_messages = {
        'password': constants.PASSWORDS_DID_NOT_MATCH,
        'old_password': constants.WRONG_OLD_PASSWORD
    }

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password_confirm')
        write_only_fields = fields

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            self.fail('password')

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            self.fail('old_password')
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
