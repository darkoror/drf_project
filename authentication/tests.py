from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from unittest.mock import patch

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status

from authentication.models import User
from drf_project.tests import BaseAPITest


class TestSignUp(BaseAPITest):
    sign_up_url = reverse('auth:sign-up')

    def setUp(self):
        self.user = self.create()
        self.data = {
            "username": "test_username",
            "email": "TEST_email@gmail.com",
            "password": "test_password",
            "password_confirm": "test_password"
        }

    @patch('authentication.tasks.send_email.delay')
    def test_register(self, delay):
        resp = self.client.post(self.sign_up_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.data["email"].lower(), resp.data["email"])
        user = User.objects.get(id=resp.data["id"])
        self.assertFalse(user.is_active)
        delay.assert_called_once()

    @patch('authentication.tasks.send_email.delay')
    def test_register_email_duplicate(self, delay):
        self.data["email"] = self.user.email
        resp = self.client.post(self.sign_up_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(email=self.data["email"]).count(), 1)
        delay.assert_not_called()

    @patch('authentication.tasks.send_email.delay')
    def test_register_wrong_confirm_password(self, delay):
        self.data["password_confirm"] = "wrong_password"
        resp = self.client.post(self.sign_up_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email=self.data["email"]).exists())
        delay.assert_not_called()


class TestActivateUser(BaseAPITest):
    activation_url = reverse('auth:activate-user')

    def setUp(self):
        self.user = self.create()
        self.user.is_active = False
        self.user.save()
        self.data = {
            "token": f"{urlsafe_base64_encode(force_bytes(self.user.id))}."
                     f"{default_token_generator.make_token(self.user)}"
        }

    def test_activate_user(self):
        resp = self.client.post(self.activation_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_user_wrong_uid(self):
        self.data["token"] = f"wrong_uid.{default_token_generator.make_token(self.user)}"
        resp = self.client.post(self.activation_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_activate_user_wrong_token(self):
        self.data["token"] = f"{urlsafe_base64_encode(force_bytes(self.user.id))}.wrong_token"
        resp = self.client.post(self.activation_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_activate_activated_user(self):
        self.user.is_active = True
        self.user.save()
        resp = self.client.post(self.activation_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_deleted_user(self):
        self.user.delete()
        resp = self.client.post(self.activation_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email=self.email).exists())


class TestPasswordReset(BaseAPITest):
    request_reset_password_url = reverse('auth:reset-password')

    def setUp(self):
        self.user = self.create()
        self.data = {
            "email": self.user.email.upper()
        }

    @patch('authentication.tasks.send_email.delay')
    def test_password_reset(self, delay):
        resp = self.client.post(self.request_reset_password_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(User.objects.filter(email=self.user.email).exists())
        delay.assert_called_once()

    @patch('authentication.tasks.send_email.delay')
    def test_password_reset_wrong_email(self, delay):
        self.data["email"] = "wrong_email@gmail.com"
        resp = self.client.post(self.request_reset_password_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        delay.assert_not_called()


class TestPasswordResetComplete(BaseAPITest):
    reset_password_url = reverse('auth:reset-password-complete')

    def setUp(self):
        self.user = self.create()
        self.new_password = "new_password"
        self.data = {
            "password": self.new_password,
            "password_confirm": self.new_password,
            "token": f"{urlsafe_base64_encode(force_bytes(self.user.id))}."
                     f"{default_token_generator.make_token(self.user)}"
        }

    def test_password_reset_complete(self):
        resp = self.client.put(self.reset_password_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.new_password))

    def test_password_reset_complete_wrong_token(self):
        self.data["token"] = f"{urlsafe_base64_encode(force_bytes(self.user.id))}.wrong_token"
        resp = self.client.put(self.reset_password_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password(self.new_password))

    def test_password_reset_complete_wrong_uid(self):
        self.data["token"] = f"wrong_uid.{default_token_generator.make_token(self.user)}"
        resp = self.client.put(self.reset_password_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password(self.new_password))

    def test_password_reset_complete_wrong_password_confirm(self):
        self.data["password_confirm"] = "wrong_password_confirm"
        resp = self.client.put(self.reset_password_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.user.check_password(self.new_password))

    def test_password_reset_complete_deleted_user(self):
        email = "random@gmail.com"
        user = self.create(email=email, username="darkor")
        self.data["token"] = f"{urlsafe_base64_encode(force_bytes(user.id))}." \
                             f"{default_token_generator.make_token(user)}"
        user.delete()
        resp = self.client.put(self.reset_password_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email=email).exists())
