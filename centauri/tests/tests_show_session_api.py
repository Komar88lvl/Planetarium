from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from centauri.models import ShowSession, AstronomyShow, ShowTheme

SHOW_SESSION_URL = reverse("centauri:showsession-list")

def sample_astronomy_show(**params) -> AstronomyShow:
    show_themes = ShowTheme(name="Test show")
    defaults = {
        "title": "Sample show",
        "description": "Sample description",
        "show_themes": show_themes,
    }
    return AstronomyShow.objects.create(**defaults)


class UnauthenticatedShowSessionTests(TestCase):
    def setUP(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SHOW_SESSION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
