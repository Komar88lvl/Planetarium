from rest_framework import viewsets

from centauri.models import (
    ShowTheme,
    PlanetariumDome,
)
from centauri.serializers import (
    ShowThemeSerializer,
    PlanetariumDomeSerializer,
)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
