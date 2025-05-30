from django.urls import path, include
from rest_framework import routers

from centauri.views import (
    ShowThemeViewSet,
    PlanetariumDomeViewSet,
    AstronomyShowViewSet,
)

router = routers.DefaultRouter()
router.register("show_themes", ShowThemeViewSet)
router.register("planetarium_domes", PlanetariumDomeViewSet)
router.register("astronomy_shows", AstronomyShowViewSet)

urlpatterns = [
    path("", include(router.urls)),
]


app_name = "centauri"
