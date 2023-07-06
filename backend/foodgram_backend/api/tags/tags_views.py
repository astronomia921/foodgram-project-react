# pylint: disable=E1101
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.tags.models import Tag

from .tags_serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = [AllowAny, ]
    serializer_class = TagSerializer
