from rest_framework import viewsets, mixins

from user_profile.serializers import ProfileSerializer, ChangePasswordSerializer


class UserProfile(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    retrieve:
    Get a user profile

    Get one user profile

    update:
    Update new user profile

    Update one user profile

    partial_update:
    Update some user profile

    Partial update one user profile
    """
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class ChangePassword(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    retrieve:
    Get a user profile

    Get one user profile

    update:
    Update new user profile

    Update one user profile

    partial_update:
    Update some user profile

    Partial update one user profile
    """
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user
