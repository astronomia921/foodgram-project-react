# pylint: disable=E1101
from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from weasyprint import HTML

from api.users.users_serializers import RecipeMinifiedSerializer

from api.filters import RecipeFilter
from api.foodgram.foodgram_serializers import (
    CreateUpdateDeleteRecipeSerializer, RecipeSerializer)
from api.pagination import MyPagination
from api.permissions import AuthorOrReadOnly

from apps.foodgram.models import Favorite, Recipe, ShoppingCart


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrReadOnly, )
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,)
    pagination_class = MyPagination
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve',):
            return RecipeSerializer
        return CreateUpdateDeleteRecipeSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()

        if self.request.user.is_authenticated:
            favorite = Favorite.objects.filter(
                user=self.request.user,
                recipe=OuterRef('pk')
            )
            shopping_cart = ShoppingCart.objects.filter(
                user=self.request.user,
                recipe=OuterRef('pk')
            )
            queryset = queryset.annotate(
                is_favorited=Exists(favorite),
                is_in_shopping_cart=Exists(shopping_cart)
            )

        return queryset

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
    )
    def download_shopping_cart(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        shopping_cart_items = request.user.shopping_cart.all()
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
        methods=['post'],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path='shopping_cart',
        url_name='shopping_cart',
    )
    def add_to_shopping_cart(self, request, pk=None):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        recipe = get_object_or_404(Recipe, pk=pk)

        if ShoppingCart.objects.filter(
                user=request.user, recipe=recipe).exists():
            return Response(
                {'error': 'Рецепт уже есть в списке покупок.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        ShoppingCart.objects.create(user=request.user, recipe=recipe)
        serializer = RecipeMinifiedSerializer(
            recipe,
            context={
                'request': request,
                'recipe': recipe
            }
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @add_to_shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk=None):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        recipe = get_object_or_404(Recipe, pk=pk)

        if not ShoppingCart.objects.filter(
                user=request.user, recipe=recipe).exists():
            return Response(
                {'error': 'Рецепт уже удалён из списка покупок.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        shopping_cart = get_object_or_404(
            ShoppingCart,
            user=request.user,
            recipe=recipe
        )
        shopping_cart.delete()
        return Response(
            {'message': 'Рецепт удалён из списка покупок.'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path='favorite',
        url_name='favorite',
    )
    def add_to_favorite(self, request, pk=None):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipe = get_object_or_404(Recipe, pk=pk)
        if Favorite.objects.filter(
                user=request.user, recipe=recipe).exists():
            return Response(
                {'error': 'Рецепт уже есть в Избранном.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = RecipeMinifiedSerializer(
                recipe,
                context={
                    'request': request,
                    'recipe': recipe
                }
            )
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)

    @add_to_favorite.mapping.delete
    def remove_from_favorite(self, request, pk=None):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        recipe = get_object_or_404(Recipe, pk=pk)
        if not Favorite.objects.filter(
                user=request.user, recipe=recipe).exists():
            return Response(
                {'error': 'Рецепт уже удалён из Избранного.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            favorite = get_object_or_404(
                Favorite,
                user=request.user,
                recipe=recipe
            )
            favorite .delete()
            return Response(
                {'message': 'Рецепт удалён из Избранного.'},
                status=status.HTTP_204_NO_CONTENT)
