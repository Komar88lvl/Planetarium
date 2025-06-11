from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


USER_MANAGE_URL = reverse("user:manage_user")


class UnauthenticatedUserManagementTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(USER_MANAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserManageTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_authenticated_user_can_update_own_profile(self):
        payload = {
            "email": "another@email.test",
            "password": "anothertestpassword",
        }

        res = self.client.put(USER_MANAGE_URL, payload)
        self.user.refresh_from_db()
        users = get_user_model().objects.all()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(users.count(), 1)
        self.assertEqual(self.user.email, payload["email"])
        self.assertTrue(self.user.check_password(payload["password"]))
