from rest_framework.test import APITestCase
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken
from django.utils import timezone

from authentication.models import User


class BaseAPITest(APITestCase):
    def create(self, username='test', email='test@mail.com', password='qwerty123456'):
        user = User.objects.create_user(username=username, email=email, password=password)
        user.last_login_date = timezone.now()
        user.is_active = True
        user.save()

        return user

    def create_and_login(self, username='test', email='test@mail.com', password='qwerty123456'):
        user = self.create(username=username, email=email, password=password)
        self.authorize(user)
        return user

    def authorize(self, user, **additional_headers):
        token = AccessToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"{api_settings.AUTH_HEADER_TYPES[0]} {token}",
            **additional_headers
        )

    def logout(self, **additional_headers):
        self.client.credentials(**additional_headers)
