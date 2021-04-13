from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profile.serializers import ProfileSerializer, ChangePasswordSerializer


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


class ChangePassword(APIView):
    """
    partial_update:
    Change the password of the user
    """
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=self.request.user, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        return self.request.user
