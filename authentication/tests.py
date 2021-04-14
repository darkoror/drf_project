from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from unittest.mock import patch

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from authentication.models import User
from drf_project.tests import BaseAPITest


class TestSignUp(BaseAPITest):

    def setUp(self):
        self.user = self.create()
        self.user.is_active = False
        self.user.save()

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

    @patch('authentication.tasks.send_email.delay')
    def test_register_with_exist_email(self, delay):
        data = {
            "username": "test_username",
            "email": self.user.email,
            "password": "test_password"
        }
        resp = self.client.post(reverse('auth:register-user'), data=data)
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(User.objects.filter(email=resp.data["email"]).exists())
        delay.assert_not_called()

    def test_activate_user(self):
        token = f"{urlsafe_base64_encode(force_bytes(self.user.email))}.{default_token_generator.make_token(self.user)}"
        resp = self.client.post(reverse('auth:email-verify'), data={"token": token})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(User.objects.get(email=self.user.email).is_active)

    def test_activate_user_wrong_token(self):
        token = "SOMERANDOMTOKEN123"
        resp = self.client.post(reverse('auth:email-verify'), data={"token": token})
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(User.objects.get(email=self.user.email).is_active)


class TestPasswordReset(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()
        self.new_password = "new password"
        self.data = {
            "token": '',
            "password": self.new_password,
            "password_repeat": self.new_password
        }

    @patch('authentication.tasks.send_email.delay')
    def test_password_reset(self, delay):
        resp = self.client.post(reverse('auth:reset-password'), data={"email": self.user.email})
        self.assertEqual(resp.status_code, 200)
        delay.assert_called_once()

    @patch('authentication.tasks.send_email.delay')
    def test_wrong_email(self, delay):
        resp = self.client.post(reverse('auth:reset-password'), data={"email": "wrong_email@gmail.com"})
        self.assertEqual(resp.status_code, 400)
        delay.assert_not_called()

    def test_set_new_password(self):
        self.data['token'] = \
            f"{urlsafe_base64_encode(force_bytes(self.user.email))}.{default_token_generator.make_token(self.user)}"

        resp = self.client.post(reverse('auth:set-new-password'), data=self.data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(self.client.login(username=self.user.username, password=self.new_password))

    def test_wrong_repeat_password(self):
        self.data['token'] = \
            f"{urlsafe_base64_encode(force_bytes(self.user.email))}.{default_token_generator.make_token(self.user)}"
        self.data['password_repeat'] = "wrong repeat password"

        resp = self.client.post(reverse('auth:set-new-password'), data=self.data)
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(self.client.login(username=self.user.username, password=self.new_password))

    def test_wrong_token(self):
        resp = self.client.post(reverse('auth:set-new-password'), data=self.data)
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(self.client.login(username=self.user.username, password=self.new_password))
