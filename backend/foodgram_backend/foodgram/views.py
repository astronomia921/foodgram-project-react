from weasyprint import HTML

from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse

from rest_framework import filters, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated)

from .filters import RecipeFilter
from .models import Recipe, ShoppingCart
from .serializers import CreatePatchDeleteRecipeSerializer, RecipeSerializer

from users.pagination import MyPagination


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,)
    pagination_class = MyPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeSerializer
        return CreatePatchDeleteRecipeSerializer

    @action(
            methods=['get'],
            detail=False,
            permission_classes=[IsAuthenticated],
            url_path='download_shopping_cart',
            url_name='download_shopping_cart',
            )
    def download_shopping_cart(self, request):
        user = request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        shopping_cart_items = ShoppingCart.objects.filter(user=user)
        recipe_instances = [item.recipe for item in shopping_cart_items]
        serializer = RecipeSerializer(
            recipe_instances, many=True, context={'request': request})

        html_string = "Список покупок с сайта Foodgram: \n"
        for recipe in serializer.data:
            for ingredient in recipe['ingredients']:
                html_string += (
                    f"{ingredient['name']}"
                    f" ({ingredient['measurement_unit']})"
                    f" - {ingredient['amount']};")
        html = HTML(string=html_string)
        result = html.write_pdf()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.pdf"')
        response.write(result)
        return response
