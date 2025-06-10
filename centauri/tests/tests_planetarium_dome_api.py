from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from centauri.models import PlanetariumDome


PLANETARIUM_DOME_URL = reverse("centauri:planetariumdome-list")


def sample_planetarium_dome(**params):
    defaults = {
        "name": "test name",
        "rows": 22,
        "seats_in_row": 33,
    }
    defaults.update(params)

    return PlanetariumDome.objects.create(**params)

class UnauthenticatedPlanetariumDomeTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLANETARIUM_DOME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
