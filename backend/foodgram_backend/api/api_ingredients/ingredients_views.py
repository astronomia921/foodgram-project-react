# pylint: disable=E1101
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny

from apps.ingredients.models import Ingredient

from api.pagination import MyPagination
from api.filters import IngredientFilter
from api.api_ingredients.ingredients_serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = MyPagination
    permission_classes = [AllowAny]
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = IngredientFilter
    search_fields = ('^name',)
