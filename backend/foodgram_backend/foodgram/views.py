from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import RecipeFilter
from .models import Recipe
from .serializers import CreatePatchDeleteRecipeSerializer, RecipeSerializer

from users.pagination import MyPagination


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,)
    pagination_class = MyPagination
    filterset_class = RecipeFilter
    search_fields = ['^author']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return CreatePatchDeleteRecipeSerializer
