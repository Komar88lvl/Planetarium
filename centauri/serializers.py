from rest_framework import serializers
from centauri.models import (
    ShowTheme,
)


class ShowThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowTheme
        fields = ("id", "name")
        read_only_fields = ("id",)
