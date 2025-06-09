from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from centauri.models import (ShowSession,
    AstronomyShow,
    ShowTheme,
    PlanetariumDome
)

SHOW_SESSION_URL = reverse("centauri:showsession-list")

def sample_astronomy_show() -> AstronomyShow:
    show_theme = ShowTheme(name="Test show")
    astronomy_show = AstronomyShow.objects.create(
        title="Test title",
        description="Test description",
    )
    astronomy_show.show_themes.add(show_theme)
    return astronomy_show

def sample_show_session(**params) -> ShowSession:
    planetarium_dome = PlanetariumDome.objects.create(
        name="Test name",
        rows=20,
        seats_in_row=25,
    )
    defaults = {
        "astronomy_show": sample_astronomy_show(),
        "planetarium_dome": planetarium_dome,
        "show_time": datetime(2025, 6, 8, 19, 0),
    }
    defaults.update(params)

    return ShowSession.objects.create(**defaults)


class UnauthenticatedShowSessionTests(TestCase):
    def setUP(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SHOW_SESSION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
