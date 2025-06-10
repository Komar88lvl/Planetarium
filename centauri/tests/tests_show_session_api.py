from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import F, Count
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from centauri.models import (
    ShowSession,
    AstronomyShow,
    ShowTheme,
    PlanetariumDome
)
from centauri.serializers import (
    ShowSessionListSerializer,
    ShowSessionRetrieveSerializer
)

SHOW_SESSION_URL = reverse("centauri:showsession-list")


def detail_url(show_session_id):
    return reverse("centauri:showsession-detail", args=(show_session_id,))


def sample_astronomy_show() -> AstronomyShow:
    show_theme_1 = ShowTheme.objects.create(name="Test show")
    show_theme_2 = ShowTheme.objects.create(name="Test second show")
    astronomy_show = AstronomyShow.objects.create(
        title="Test title",
        description="Test description",
    )
    astronomy_show.show_themes.add(show_theme_1, show_theme_2)
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
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SHOW_SESSION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedShowSessionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_show_session_list(self):
        sample_show_session()

        res = self.client.get(SHOW_SESSION_URL)
        show_sessions = ShowSession.objects.annotate(
            available_places=(
                    F("planetarium_dome__rows") *
                    F("planetarium_dome__seats_in_row") -
                    Count("tickets")
            )
        )
        serializer = ShowSessionListSerializer(show_sessions, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_show_sessions_by_show_date(self):
        show_session = sample_show_session()

        res = self.client.get(
            SHOW_SESSION_URL,
            {"show_date": f"{show_session.show_time.date()}"}
        )
        show_session = ShowSession.objects.annotate(
            available_places=(
                    F("planetarium_dome__rows") *
                    F("planetarium_dome__seats_in_row") -
                    Count("tickets")
            )
        )
        serializer = ShowSessionListSerializer(show_session, many=True)

        self.assertIn(serializer.data[0], res.data["results"])

    def test_filter_show_sessions_by_planetarium_dome_name(self):
        show_session = sample_show_session()

        res = self.client.get(
            SHOW_SESSION_URL,
            {"planetarium_dome": "name"}
        )
        show_session = ShowSession.objects.annotate(
            available_places=(
                    F("planetarium_dome__rows") *
                    F("planetarium_dome__seats_in_row") -
                    Count("tickets")
            )
        )

        serializer = ShowSessionListSerializer(show_session, many=True)

        self.assertIn(serializer.data[0], res.data["results"])

    def test_filter_show_sessions_by_astronomy_show_title(self):
        show_session = sample_show_session()

        res = self.client.get(
            SHOW_SESSION_URL,
            {"astronomy_show": "title"}
        )
        show_session = ShowSession.objects.annotate(
            available_places=(
                    F("planetarium_dome__rows") *
                    F("planetarium_dome__seats_in_row") -
                    Count("tickets")
            )
        )

        serializer = ShowSessionListSerializer(show_session, many=True)

        self.assertIn(serializer.data[0], res.data["results"])

    def test_retrieve_show_session_detail(self):
        show_session = sample_show_session()

        url = detail_url(show_session.id)

        res = self.client.get(url)

        serializer = ShowSessionRetrieveSerializer(show_session)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_show_session_forbidden(self):
        planetarium_dome = PlanetariumDome.objects.create(
            name="test dom name",
            rows=33,
            seats_in_row=41,
        )
        payload = {
            "show_time": datetime(2024, 11, 16, 13, 30),
            "astronomy_show": sample_astronomy_show(),
            "planetarium_dome": planetarium_dome
        }

        res = self.client.post(SHOW_SESSION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminShowSessionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.test",
            password="adminpassword",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_show_session(self):
        planetarium_dome = PlanetariumDome.objects.create(
            name="dom name",
            rows=33,
            seats_in_row=22,
        )
        payload = {
            "show_time": timezone.make_aware(datetime(2024, 11, 23, 7, 15)),
            "astronomy_show": sample_astronomy_show().id,
            "planetarium_dome": planetarium_dome.id
        }

        res = self.client.post(SHOW_SESSION_URL, payload)

        show_session = ShowSession.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for key in payload:
            model_value = getattr(show_session, key)
            if hasattr(model_value, "id"):
                model_value = model_value.id
            self.assertEqual(payload[key], model_value)
