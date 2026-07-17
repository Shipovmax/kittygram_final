from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import BaseSerializer

from .models import Achievement, Cat
from .serializers import AchievementSerializer, CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    """CRUD endpoint for cat cards, scoped to the requesting owner."""

    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer: BaseSerializer) -> None:
        """Attach the authenticated request user as the cat's owner."""
        serializer.save(owner=self.request.user)


class AchievementViewSet(viewsets.ModelViewSet):
    """CRUD endpoint for achievement tags (unpaginated, small dataset)."""

    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    pagination_class = None
