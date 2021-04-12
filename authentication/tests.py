from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from unittest.mock import patch

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from authentication.models import User
from drf_project.tests import BaseAPITest


class TestSignUp(BaseAPITest):

    @patch('authentication.tasks.send_email.delay')
    def test_register(self, delay):
        data = {
            "username": "test_username",
            "email": "TEST_email@gmail.com",
            "password": "test_password"
        }
        resp = self.client.post(reverse('auth:register-user'), data=data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(data["email"].lower(), resp.data["email"])
        self.assertTrue(User.objects.filter(email=resp.data["email"]).exists())
        self.assertFalse(User.objects.get(email=resp.data["email"]).is_active)
        delay.assert_called_once()

        user = User.objects.get(email=resp.data["email"])
        token = f"{urlsafe_base64_encode(force_bytes(user.email))}.{default_token_generator.make_token(user)}"
        resp2 = self.client.post(reverse('auth:email-verify'), data={"token": token})
        self.assertEqual(resp2.status_code, 200)
        self.assertTrue(User.objects.get(email=resp.data["email"]).is_active)


class TestPasswordReset(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()
        self.user.save()
        self.new_password = "new password"

    @patch('authentication.tasks.send_email.delay')
    def test_password_reset(self, delay):
        data = {
            "email": self.user.email
        }
        resp = self.client.post(reverse('auth:reset-password'), data=data)
        self.assertEqual(resp.status_code, 200)
        delay.assert_called_once()

        token = f"{urlsafe_base64_encode(force_bytes(self.user.email))}.{default_token_generator.make_token(self.user)}"
        data2 = {
            "token": token,
            "password": self.new_password,
            "password_repeat": self.new_password
        }
        resp2 = self.client.post(reverse('auth:set-new-password'), data=data2)
        self.assertEqual(resp2.status_code, 200)
        self.assertTrue(self.client.login(username=self.user.username, password=self.new_password))
