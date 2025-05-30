from rest_framework import viewsets

from centauri.models import ShowTheme
from centauri.serializers import ShowThemeSerializer


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
