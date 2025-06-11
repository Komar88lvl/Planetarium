import tempfile
import os

from PIL import Image
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from centauri.models import AstronomyShow, ShowTheme
from centauri.serializers import AstronomyShowListSerializer

ASTRONOMY_SHOW_URL = reverse("centauri:astronomyshow-list")


def image_upload_url(astronomy_show_id):
    return reverse(
        "centauri:astronomyshow-upload-poster",
        args=[astronomy_show_id]
    )


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

        serializer = AstronomyShowListSerializer(
            [astronomy_show, astronomy_show_2],
            many=True
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_astronomy_show_by_show_themes(self):
        show_theme_2 = ShowTheme.objects.create(name="Test another show")
        show_theme_3 = ShowTheme.objects.create(name="Not match")

        astronomy_show = sample_astronomy_show()

        astronomy_show_2 = AstronomyShow.objects.create(
            title="Test second title",
            description="Test second description",
        )
        astronomy_show_2.show_themes.set([show_theme_2])

        astronomy_show_3 = AstronomyShow.objects.create(
            title="Test third title",
            description="Test third description",
        )
        astronomy_show_3.show_themes.set([show_theme_3])

        res = self.client.get(
            ASTRONOMY_SHOW_URL,
            {"show_themes": "show"}
        )

        serializer = AstronomyShowListSerializer(astronomy_show)
        serializer_2 = AstronomyShowListSerializer(astronomy_show_2)
        serializer_3 = AstronomyShowListSerializer(astronomy_show_3)

        self.assertIn(serializer.data, res.data["results"])
        self.assertIn(serializer_2.data, res.data["results"])
        self.assertNotIn(serializer_3.data, res.data["results"])


class AstronomyShowImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@test.com", "testpassword"
        )
        self.client.force_authenticate(self.user)
        self.astronomy_show = sample_astronomy_show()

    def tearDown(self):
        self.astronomy_show.poster.delete()

    def test_upload_poster_to_astronomy_show(self):
        url = image_upload_url(self.astronomy_show.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {"poster": ntf}, format="multipart")
        self.astronomy_show.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("poster", res.data)
        self.assertTrue(os.path.exists(self.astronomy_show.poster.path))
