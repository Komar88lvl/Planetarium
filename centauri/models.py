from django.db import models


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"Show theme: {self.name}"


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField
    show_themes = models.ManyToManyField(
        ShowTheme,
        related_name="astronomy_shows",
    )

    def __str__(self):
        return f"Astronomy show: {self.title}"
