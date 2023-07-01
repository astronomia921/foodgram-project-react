# pylint: disable=E1101
import django_filters as filters

from apps.foodgram.models import Recipe
from apps.ingredients.models import Ingredient
from apps.tags.models import Tag


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter(
        field_name='author__id'
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',
                  'is_favorited',
                  'is_in_shopping_cart',
                  )

    def filter_is_favorited(self, queryset, name, value):
        if not self.request.user:
            return Recipe.objects.none()
        if value:
            return queryset.filter(favorite__user=self.request.user)
        else:
            return queryset.exclude(favorite__user=self.request.user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if not self.request.user:
            return Recipe.objects.none()
        if value:
            return queryset.filter(shopping_cart__user=self.request.user)
        else:
            return queryset.exclude(shopping_cart__user=self.request.user)


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
