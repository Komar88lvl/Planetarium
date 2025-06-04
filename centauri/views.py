from datetime import datetime

from rest_framework import viewsets

from centauri.models import (
    ShowTheme,
    PlanetariumDome,
    AstronomyShow,
    ShowSession,
    Reservation,
)
from centauri.serializers import (
    ShowThemeSerializer,
    PlanetariumDomeSerializer,
    AstronomyShowSerializer,
    ShowSessionSerializer,
    AstronomyShowListSerializer,
    ShowSessionListSerializer,
    AstronomyShowRetrieveSerializer,
    PlanetariumDomeListSerializer,
    ShowSessionRetrieveSerializer,
    ReservationSerializer,
)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PlanetariumDomeListSerializer

        return PlanetariumDomeSerializer


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.prefetch_related("show_themes")

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer
        elif self.action == "retrieve":
            return AstronomyShowRetrieveSerializer

        return AstronomyShowSerializer

    def get_queryset(self):
        queryset = self.queryset
        show_themes = self.request.query_params.get("show_themes")

        if show_themes:
            queryset = queryset.filter(
                show_themes__name__icontains=show_themes
            )

        return queryset.distinct()


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        elif self.action == "retrieve":
            return ShowSessionRetrieveSerializer

        return ShowSessionSerializer

    def get_queryset(self):
        show_date = self.request.query_params.get("show_date")
        astronomy_show = self.request.query_params.get("astronomy_show")
        planetarium_dome = self.request.query_params.get("planetarium_dome")

        queryset = self.queryset

        if show_date:
            show_date = datetime.strptime(show_date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=show_date)

        if astronomy_show:
            queryset = queryset.filter(astronomy_show__title__icontains=astronomy_show)

        if planetarium_dome:
            queryset = queryset.filter(planetarium_dome__name__icontains=planetarium_dome)

        if self.action == "list":
            return queryset.select_related()

        return queryset


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
