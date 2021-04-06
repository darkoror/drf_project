from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.serializers import SignUpSerializer, LogoutSerializer


class SignUpView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
