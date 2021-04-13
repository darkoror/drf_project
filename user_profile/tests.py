from django.urls import reverse

from drf_project.tests import BaseAPITest


class TestUserProfile(BaseAPITest):

    def setUp(self):
        self.user = self.create_and_login()

    def test_retrieve_user_profile(self):
        resp = self.client.get(reverse('user-profile:get-user-profile'))
        self.assertEqual(resp.status_code, 200)

    def test_update_user_profile(self):
        data = {
            "username": "updated username"
        }
        resp = self.client.patch(reverse('user-profile:update-user-profile'), data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data["username"], resp.data["username"])

    def test_change_password(self):
        data = {
            "old_password": 'qwerty123456',
            "new_password": "new password",
            "confirmed_password": "new password"
        }
        resp = self.client.post(reverse('user-profile:change-password'), data=data)
        self.assertEqual(resp.status_code, 204)
        self.client.logout()
        self.assertTrue(self.client.login(username=self.user.username, password=data["new_password"]))
