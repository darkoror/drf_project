from django.urls import reverse
from rest_framework import status

from drf_project.tests import BaseAPITest


class TestUserProfile(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()

    def test_retrieve_user_profile(self):
        resp = self.client.get(reverse('user-profile:get-user-profile'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data['id'], self.user.id)
        self.assertEqual(data['username'], self.username)
        self.assertEqual(data['email'], self.email)

    def test_update_user_profile(self):
        data = {
            "username": "updated username",
        }
        resp = self.client.patch(reverse('user-profile:update-user-profile'), data=data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(data["username"], resp.data["username"])


class TestChangePassword(BaseAPITest):
    change_password_url = reverse('user-profile:change-password')

    def setUp(self):
        self.user = self.create_and_login()
        self.data = {
            "old_password": self.password,
            "password": "new password",
            "password_confirm": "new password"
        }

    def test_change_password(self):
        resp = self.client.put(self.change_password_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.data["password"]))

    def test_change_password_wrong_old_password(self):
        self.data["old_password"] = "wrong"
        resp = self.client.put(self.change_password_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password(self.data["password"]))

    def test_profile_password_change_did_not_match(self):
        self.data["password_confirm"] = "wrong"
        resp = self.client.put(self.change_password_url, data=self.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password(self.data["password"]))
