from datetime import datetime

from django.db.models import Count, F
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

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
    ReservationListSerializer,
    AstronomyShowPosterSerializer,
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
        elif self.action == "upload_poster":
            return AstronomyShowPosterSerializer

        return AstronomyShowSerializer

    def get_queryset(self):
        queryset = self.queryset
        show_themes = self.request.query_params.get("show_themes")

        if show_themes:
            queryset = queryset.filter(
                show_themes__name__icontains=show_themes
            )

        return queryset.distinct()

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-poster",
        permission_classes=[IsAdminUser],
    )
    def upload_poster(self, request, pk=None):
        astronomy_show = self.get_object()
        serializer = self.get_serializer(astronomy_show, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="show_themes",
                type=OpenApiTypes.STR,
                description="Filter by movie show theme name "
                            "(ex. ?show_themes=galaxies)",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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
            queryset = queryset.filter(
                astronomy_show__title__icontains=astronomy_show
            )

        if planetarium_dome:
            queryset = queryset.filter(
                planetarium_dome__name__icontains=planetarium_dome
            )

        if self.action == "retrieve":
            return queryset.select_related()
        elif self.action == "list":
            queryset = (
                queryset
                .select_related()
                .annotate(
                    available_places=(
                            F("planetarium_dome__rows")
                            * F("planetarium_dome__seats_in_row")
                            - Count("tickets")
                    )
                )
            )

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="show_date",
                type=OpenApiTypes.STR,
                description="Filter by show session date "
                            "(ex. ?show_date=2025-06-21)",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == "list":
            queryset = queryset.prefetch_related(
                "tickets__show_session__planetarium_dome",
                "tickets__show_session__astronomy_show",

            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            serializer = ReservationListSerializer

        return serializer
