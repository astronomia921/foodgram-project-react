import django_filters as filters

from tags.models import Tag
from .models import Recipe

STATUS_CHOICES = (
    ('0', 'False'),
    ('1', 'True')
)


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.ChoiceFilter(
        choices=STATUS_CHOICES,
        method='filter_is_favorited')
    is_in_shopping_cart = filters.ChoiceFilter(
        choices=STATUS_CHOICES,
        method='filter_is_in_shopping_cart')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if not user:
            return Recipe.objects.none()
        if value == '1':
            return queryset.filter(favorite__user=user)
        elif value == '0':
            return queryset.exclude(favorite__user=user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if not user:
            return Recipe.objects.none()
        if value == '1':
            return queryset.filter(shopping_cart__user=user)
        elif value == '0':
            return queryset.exclude(shopping_cart__user=user)
