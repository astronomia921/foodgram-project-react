import base64

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

from foodgram_backend.settings import (
    MAX_LENGTH_NAME, MAX_LENGTH_DIGITS,
    MAX_DECIMAL_PLACES, LENGTH_HEADER)

from ingredients.models import Ingredient
from tags.models import Tag


class Recipe(models.Model):
    """
    Рецепт блюда.
    Все поля обязательны.
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        help_text='Автор рецепта',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название',
        help_text='Введите название рецепта'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        help_text='Загрузите изображение',
        upload_to='recipes/%Y/%m/%d',
        blank=True
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
        help_text='Добавьте описание рецепта',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации рецепта',
        auto_now_add=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipe_ingredient',
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipe_tag',
        through='RecipeTags'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=(
            MinValueValidator(
                1,
                message='Время приготовление должны быть >= 1 минуте.'),
        ),
        help_text='Введите время приготовления (ед. измерения в минутах))',
    )

    class Meta:
        ordering = ['-pub_date']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name_plural = 'Рецепты'
        verbose_name = 'Рецепт'

    def __str__(self):
        return self.name[:LENGTH_HEADER]


class RecipeIngredient(models.Model):
    """
    Промежуточная модель для ингредиентов.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    quantity = models.DecimalField(
        max_digits=MAX_LENGTH_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        validators=[
            MinValueValidator(
                1, 'Колличество ингредиента в рецептне должно быть >= 1.'
            )
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f"В рецепте '{self.recipe}' есть ингредиент '{self.ingredient}'"


class RecipeTags(models.Model):
    """
    Промежуточная модель для тегов.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Тег'

    def __str__(self):
        return f"У рецепта '{self.recipe}' есть тег '{self.tag}'"


class Favorite(models.Model):
    """
    Модель избранных рецептов.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorite',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

        ordering = ['recipe']
        indexes = [
            models.Index(fields=['user', 'recipe']),
            ]

    def __str__(self):
        return (f"Рецепт: '{self.recipe}' добавлен в избранное"
                f"пользователем: '{self.user.username}'")


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_shopping_list',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Cписок покупок'
        verbose_name_plural = 'Список покупок'

        ordering = ['recipe']
        indexes = [
            models.Index(fields=['user', 'recipe']),
            ]

    def __str__(self):
        return (f"Рецепт: '{self.recipe}' добавлен в список покупок"
                f"пользователю: '{self.user.username}'")
