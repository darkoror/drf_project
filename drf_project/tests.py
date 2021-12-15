from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from authentication.models import User


class BaseAPITest(APITestCase):
    email = 'test@mail.com'
    username = 'Pablo'
    password = 'qwerty12345'

    def create(self, username=username, email=email, password=password):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_active = True
        user.save()
        return user

    def create_and_login(self, username=username, email=email, password=password):
        user = self.create(username=username, email=email, password=password)
        self.authorize(user)
        return user

    def authorize(self, user, **additional_headers):
        token = AccessToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"JWT {token}",
            **additional_headers
        )

    def logout(self, **additional_headers):
        self.client.credentials(**additional_headers)
