from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    show_themes = models.ManyToManyField(
        ShowTheme,
        related_name="astronomy_shows",
    )

    def __str__(self):
        return self.title


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
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

    def __str__(self):
        return (
            f"row: {self.row}, seat: {self.seat}, "
            f"reservation: {self.reservation}"
        )
