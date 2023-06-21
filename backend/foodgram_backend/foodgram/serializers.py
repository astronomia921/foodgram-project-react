from rest_framework import serializers

from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer

from .models import Recipe, RecipeIngredient, Favorite, ShoppingCart


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(
        method_name='get_id')
    name = serializers.SerializerMethodField(
        method_name='get_name')
    measurement_unit = serializers.SerializerMethodField(
        method_name='get_measurement_unit'
    )

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients'
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_ingredients(self, obj):
        list_ingredients = RecipeIngredient.objects.filter(recipe=obj)
        serializers = RecipeIngredientsSerializer(
            list_ingredients,
            many=True,
            read_only=True
        )
        return serializers.data

    def get_is_favorited(self, obj):
        user = self.context.get('user')
        if not user:
            return False
        return Favorite.objects.filter(user=user, author=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('user')
        if not user:
            return False
        return ShoppingCart.objects.filter(user=user, author=obj).exists()
