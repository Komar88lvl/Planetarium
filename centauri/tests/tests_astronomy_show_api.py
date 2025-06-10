from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from centauri.models import AstronomyShow, ShowTheme
from centauri.serializers import AstronomyShowListSerializer

ASTRONOMY_SHOW_URL = reverse("centauri:astronomyshow-list")


def sample_astronomy_show() -> AstronomyShow:
    show_theme_1 = ShowTheme.objects.create(name="Test show")
    show_theme_2 = ShowTheme.objects.create(name="Test second show")
    astronomy_show = AstronomyShow.objects.create(
        title="Test title",
        description="Test description",
    )
    astronomy_show.show_themes.add(show_theme_1, show_theme_2)
    return astronomy_show


class UnauthenticatedSAstronomyShowTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ASTRONOMY_SHOW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAstronomyShowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_astronomy_show_list(self):
        show_theme_1 = ShowTheme.objects.create(name="Test second")
        show_theme_2 = ShowTheme.objects.create(name="Test third show")
        astronomy_show = sample_astronomy_show()
        astronomy_show_2 = AstronomyShow.objects.create(
        title="second title",
        description="second description",
        )
        astronomy_show.show_themes.add(show_theme_1, show_theme_2)

        res = self.client.get(ASTRONOMY_SHOW_URL)

        serializer = AstronomyShowListSerializer([astronomy_show, astronomy_show_2], many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)
