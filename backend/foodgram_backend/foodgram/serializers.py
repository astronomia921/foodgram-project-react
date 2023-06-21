from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer
from tags.models import Tag
from ingredients.models import Ingredient

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
    author = CustomUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault())
    tags = TagSerializer(
        many=True,
        read_only=True)

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


class MiniRecipeIngredientSerialiser(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')

    def validate_id(self, value):
        if not value:
            raise serializers.ValidationError(
                {
                    'error': 'Необходимо указать id ингредиента.'
                    }
                )
        return value

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(
                {
                    'error': 'Колличество ингредиента должно быть >= 1.'
                    }
                )
        return value


class CreatePatchDeleteRecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault())
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
            'Они не должны повторяться и быть больше чем 1')
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
        fields = ('id', 'author', 'ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time')
        extra_kwargs = {
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
        if len(value) != len(set(value)):
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
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        for tag_data in tags_data:
            recipe.tags.add(tag_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        instance.name = validated_data.get('name',
                                           instance.name)
        instance.text = validated_data.get('text',
                                           instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        instance.image = validated_data.get('image',
                                            instance.image)
        instance.tags.set(tags_data)
        instance.ingredients.all().delete()
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=instance, **ingredient_data)
        instance.save()
        return instance

    def destroy(self, instance):
        instance.delete()
