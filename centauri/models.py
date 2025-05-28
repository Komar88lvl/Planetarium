from django.db import models


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)
