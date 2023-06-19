from rest_framework import serializers

from .models import Recipe

from ingredients.serializers import IngredientSerializer
from users.serializers import CreateUserSerializer
from tags.serializers import TagSerializer


class RecipeSerializer(serializers.ModelSerializer):
    author = CreateUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('author', 'ingredients', 'tags',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'text', 'image', 'cooking_time')


class RecipeFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
