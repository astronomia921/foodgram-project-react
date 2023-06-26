from weasyprint import HTML

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated, )
from rest_framework.response import Response

from users.pagination import MyPagination
from users.serializers import RecipeMinifiedSerializer

from .filters import RecipeFilter
from .models import Favorite, Recipe, ShoppingCart
from .serializers import CreateUpdateDeleteRecipeSerializer, RecipeSerializer
from .permissions import IsAuthorOrAdmin


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrAdmin, )
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,)
    pagination_class = MyPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeSerializer
        return CreateUpdateDeleteRecipeSerializer

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
        ingredients_dict = {}
        for recipe in serializer.data:
            for ingredient in recipe['ingredients']:
                name = ingredient['name']
                measurement_unit = ingredient['measurement_unit']
                amount = ingredient['amount']
                key = f"{name} ({measurement_unit})"
                if key in ingredients_dict:
                    ingredients_dict[key] += amount
                else:
                    ingredients_dict[key] = amount
        html_string = (
            f"Список покупок пользователя {request.user.username}: \n")
        for key, value in ingredients_dict.items():
            html_string += f"{key} - {value}\n"
        html = HTML(string=html_string)
        result = html.write_pdf()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.pdf"')
        response.write(result)
        return response

    @action(
            methods=['post', 'delete'],
            detail=True,
            permission_classes=[IsAuthenticated],
            url_path='shopping_cart',
            url_name='shopping_cart',
            )
    def shopping_cart(self, request, pk=None):
        user = request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if ShoppingCart.objects.filter(
                    user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Рецепт уже есть в списке покупок.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                ShoppingCart.objects.create(user=user, recipe=recipe)
                serializer = RecipeMinifiedSerializer(
                    recipe,
                    context={
                        'request': request,
                        'recipe': recipe
                        }
                )
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if not ShoppingCart.objects.filter(
                    user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Рецепт уже удалён из списка покупок.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                shopping_cart = get_object_or_404(
                    ShoppingCart,
                    user=user,
                    recipe=recipe
                )
                shopping_cart.delete()
                return Response(
                    {'message': 'Рецепт удалён из списка покупок.'},
                    status=status.HTTP_204_NO_CONTENT)

    @action(
            methods=['post', 'delete'],
            detail=True,
            permission_classes=[IsAuthenticated],
            url_path='favorite',
            url_name='favorite',
            )
    def favorite(self, request, pk=None):
        user = request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if Favorite.objects.filter(
                    user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Рецепт уже есть в Избранном.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                Favorite.objects.create(user=user, recipe=recipe)
                serializer = RecipeMinifiedSerializer(
                    recipe,
                    context={
                        'request': request,
                        'recipe': recipe
                        }
                )
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if not Favorite.objects.filter(
                    user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Рецепт уже удалён из Избранного.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                favorite = get_object_or_404(
                    Favorite,
                    user=user,
                    recipe=recipe
                )
                favorite .delete()
                return Response(
                    {'message': 'Рецепт удалён из Избранного.'},
                    status=status.HTTP_204_NO_CONTENT)
