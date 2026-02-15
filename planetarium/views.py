from datetime import datetime
from django.db.models import F, Count
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
)
from planetarium.serializers import (
    ShowThemeSerializer,
    AstronomyShowSerializer,
    AstronomyShowListSerializer,
    PlanetariumDomeSerializer,
    ShowSessionSerializer,
    ShowSessionListSerializer,
    ReservationSerializer,
    ReservationListSerializer,
)

class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer

class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer
        return AstronomyShowSerializer

    def get_queryset(self):
        queryset = self.queryset
        themes = self.request.query_params.get("themes")
        if themes:
            themes_ids = [int(str_id) for str_id in themes.split(",")]
            queryset = queryset.filter(themes__id__in=themes_ids)
        return queryset.distinct()

class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer

class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = (
        ShowSession.objects.all()
        .select_related("astronomy_show", "planetarium_dome")
        .annotate(
            tickets_available=(
                F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row")
                - Count("tickets")
            )
        )
    )
    serializer_class = ShowSessionSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        return ShowSessionSerializer

class ReservationPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Reservation.objects.prefetch_related("tickets__show_session__astronomy_show")
    serializer_class = ReservationSerializer
    pagination_class = ReservationPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer
        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)