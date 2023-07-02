# pylint: disable=E1101

from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from apps.foodgram.models import Recipe, RecipeIngredient
from apps.ingredients.models import Ingredient
from apps.tags.models import Tag

from api.api_users.users_serializers import CustomUserSerializer
from api.api_tags.tags_serializers import TagSerializer


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients'
    )
    is_favorited = serializers.BooleanField(
        read_only=True,
        default=False
    )
    is_in_shopping_cart = serializers.BooleanField(
        read_only=True,
        default=False
    )

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time',)

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        serializer = RecipeIngredientsSerializer(ingredients, many=True)
        return serializer.data


class MiniRecipeIngredientSerialiser(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount',)

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(
                {
                    'error': 'Колличество ингредиента должно быть >= 1.'
                }
            )
        return value


class CreateUpdateDeleteRecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(
        required=False,
        allow_null=True,
        label='Изображение',
        help_text='Добавьте изображение (необязательно)'
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        label='Тег',
        help_text='Добавьте тег (больше 1)'
    )
    ingredients = MiniRecipeIngredientSerialiser(
        style={'base_template': 'input.html'},
        many=True,
        label='Ингредиент',
        help_text=(
            'Добавьте ингредиенты.'
            ' Они не должны повторяться и быть не меньше 1')
    )
    cooking_time = serializers.IntegerField(
        label='Время приготовления',
        help_text='Добавьте время приготовления (больше 1 минуты)'
    )
    name = serializers.CharField(
        label='Название рецепта',
        help_text='Добавьте название рецепта'
    )

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'ingredients',
                  'tags', 'image', 'name',
                  'text', 'cooking_time')
        extra_kwargs = {
            'name': {'required': True},
            'ingredients': {'required': True},
            'tags': {'required': True},
            'text': {'required': True},
            'cooking_time': {'required': True},
        }

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                {
                    'error': 'Нужно указать хотя бы 1 ингредиента в рецепте.'
                }
            )
        ids = [item['id'] for item in value]
        if len(ids) != len(set(ids)):
            raise serializers.ValidationError(
                {
                    'error': 'Ингредиенты в рецепте должны быть уникальными.'
                }
            )
        return value

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(
                {
                    'error': 'Нужно добавить хотя бы 1 тег.'
                }
            )
        return value

    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError(
                {
                    'error': 'Время приготовление должны быть >= 1 минуте.'
                }
            )
        return value

    def validate_name(self, value):
        if len(value) > 200:
            raise serializers.ValidationError(
                {
                    'error': 'Название должно быть <= 200 символам.'
                }
            )
        return value

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.set(tags)

        ingredients = validated_data.pop('ingredients', None)
        if ingredients is not None:
            instance.ingredients.clear()

            for ingredient in ingredients:
                amount = ingredient['amount']
                ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])

                RecipeIngredient.objects.update_or_create(
                    recipe=instance,
                    ingredient=ingredient,
                    defaults={'amount': amount}
                )

        return super().update(instance, validated_data)

    def destroy(self, instance):
        instance.delete()

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data
