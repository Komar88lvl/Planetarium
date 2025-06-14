from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from centauri.models import PlanetariumDome
from centauri.serializers import (
    PlanetariumDomeListSerializer,
    PlanetariumDomeSerializer
)

PLANETARIUM_DOME_URL = reverse("centauri:planetariumdome-list")


def detail_url(planetarium_dome_id):
    return reverse(
        "centauri:planetariumdome-detail",
        args=(planetarium_dome_id,)
    )


def sample_planetarium_dome(**params):
    defaults = {
        "name": "test name",
        "rows": 22,
        "seats_in_row": 33,
    }
    defaults.update(params)

    return PlanetariumDome.objects.create(**defaults)


class UnauthenticatedPlanetariumDomeTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLANETARIUM_DOME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlanetariumDomeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_planetarium_dome_list(self):
        planetarium_dome = sample_planetarium_dome()

        res = self.client.get(PLANETARIUM_DOME_URL)

        serializer = PlanetariumDomeListSerializer(planetarium_dome)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"][0], serializer.data)

    def test_retrieve_planetarium_dome_detail(self):
        planetarium_dome = sample_planetarium_dome()

        url = detail_url(planetarium_dome.id)

        res = self.client.get(url)

        serializer = PlanetariumDomeSerializer(planetarium_dome)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
