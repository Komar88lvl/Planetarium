from django.conf import settings
from django.db import models


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"Show theme: {self.name}"


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    show_themes = models.ManyToManyField(
        ShowTheme,
        related_name="astronomy_shows",
    )

    def __str__(self):
        return f"Astronomy show: {self.title}"


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.ImageField()
    seats_in_row = models.ImageField()

    def __str__(self):
        return f"Hall: {self.name}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
