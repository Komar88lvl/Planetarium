from rest_framework import serializers
from centauri.models import (
    ShowTheme,
    PlanetariumDome,
    AstronomyShow,
    ShowSession,
)


class ShowThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowTheme
        fields = ("id", "name")


class PlanetariumDomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class PlanetariumDomeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanetariumDome
        fields = ("name", "capacity")


class AstronomyShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "show_themes")


class AstronomyShowListSerializer(AstronomyShowSerializer):
    show_themes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )


class AstronomyShowRetrieveSerializer(AstronomyShowSerializer):
    show_themes = ShowThemeSerializer(many=True)


class ShowSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time")


class ShowSessionListSerializer(ShowSessionSerializer):
    astronomy_show = serializers.CharField(source="astronomy_show.title", read_only=True)
    planetarium_dome = serializers.CharField(source="planetarium_dome.name", read_only=True)
