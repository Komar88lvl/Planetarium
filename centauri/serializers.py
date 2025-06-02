from rest_framework import serializers
from centauri.models import (
    ShowTheme,
    PlanetariumDome,
    AstronomyShow,
    ShowSession,
    Ticket,
    Reservation,
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
    astronomy_show = serializers.CharField(
        source="astronomy_show.title",
        read_only=True
    )
    planetarium_dome = serializers.CharField(
        source="planetarium_dome.name",
        read_only=True
    )


class ShowSessionRetrieveSerializer(ShowSessionSerializer):
    astronomy_show = AstronomyShowRetrieveSerializer(
        many=False,
        read_only=True
    )
    planetarium_dome = PlanetariumDomeSerializer(
        many=False,
        read_only=True
    )


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        reservation = Reservation.objects.create(**validated_data)
        for ticket_data in tickets_data:
            Ticket.objects.create(reservation=reservation, **ticket_data)
        return reservation
