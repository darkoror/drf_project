from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from authentication.models import User
from user_profile.serializers import ProfileSerializer, PasswordChangeSerializer


class UserProfile(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    retrieve:
    Get a user profile

    update:
    Update the user profile

    partial_update:
    Update some fields of the user profile
    """
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class PasswordChangeView(mixins.UpdateModelMixin, GenericViewSet):
    """
    update:
    Password change

    Update password for current authenticated user
    """

    queryset = User.objects.all()
    serializer_class = PasswordChangeSerializer

    def get_object(self):
        return self.request.user
