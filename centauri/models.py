import pathlib
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.text import slugify


class ShowTheme(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


def astronomy_show_poster_path(
        instance: "AstronomyShow",
        filename: str
) -> pathlib.Path:
    filename = (f"{slugify(instance.title)}-{uuid.uuid4()}"
                + pathlib.Path(filename).suffix)
    return pathlib.Path("upload/astronomy_shows/") / pathlib.Path(filename)


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    show_themes = models.ManyToManyField(
        ShowTheme,
        related_name="astronomy_shows",
    )
    poster = models.ImageField(null=True, upload_to=astronomy_show_poster_path)

    def __str__(self):
        return self.title


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        AstronomyShow,
        on_delete=models.CASCADE,
        related_name="show_sessions",
    )
    planetarium_dome = models.ForeignKey(
        PlanetariumDome,
        on_delete=models.CASCADE,
        related_name="show_sessions",
    )
    show_time = models.DateTimeField()

    def __str__(self):
        return (
            f"show: {self.astronomy_show}, "
            f"hall: {self.planetarium_dome}, "
            f"time: {self.show_time}"
        )


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations",
    )

    def __str__(self):
        return f"Client name: {self.user}, created: {self.created_at}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(
        ShowSession,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="tickets",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["seat", "row", "show_session"],
                name="unique_ticket_seat_row_show_session"
            )
        ]

    @staticmethod
    def validate_ticket(row, seat, planetarium_dome, error_to_raise):
        for (ticket_attr_value,
             ticket_attr_name,
             planetarium_dome_attr_name
             ) in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(planetarium_dome, planetarium_dome_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name:
                            f"{ticket_attr_name} "
                            f"number must be in available range: "
                            f"(1, {planetarium_dome_attr_name}): "
                            f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.show_session.planetarium_dome,
            ValidationError,
        )

    def __str__(self):
        return (
            f"row: {self.row}, seat: {self.seat}, "
            f"reservation: {self.reservation}"
        )
