from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny

from .serializers import IngredientSerializer
from .models import Ingredient
from .filters import IngredientFilter

from users.pagination import MyPagination


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = MyPagination
    permission_classes = [AllowAny]
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = IngredientFilter
    search_fields = ('^name',)
