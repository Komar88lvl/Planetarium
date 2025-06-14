from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse


USER_REGISTRATION_URL = reverse("user:create")


class UnauthenticatedRegister(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_unauthenticate_register(self):
        payload = {
            "email": "user@test.test",
            "password": "testpassword",
        }

        res = self.client.post(USER_REGISTRATION_URL, payload)
        user = get_user_model().objects.get(email=payload["email"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, payload["email"])
        self.assertTrue(user.check_password(payload["password"]))


class SuperUserRegister(TestCase):
    def test_create_superuser_with_email_only(self):
        email = "super@user.test"
        password = "superpassword"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.username, None)
