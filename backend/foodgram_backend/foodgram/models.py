from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from foodgram_backend.settings import (
    MAX_LENGTH_NAME, MAX_LENGTH_UNIT,
    MAX_LENGTH_TAG, MAX_LENGTH_HEX,
    MAX_LENGTH_SLUG, MAX_LENGTH_DIGITS,
    MAX_DECIMAL_PLACES, LENGTH_HEADER)


class Ingredient(models.Model):
    """
    Ингредиенты.
    """
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=MAX_LENGTH_NAME
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        help_text='Единицы измерения: шт, ложки, стакан, кг, щепотка',
        max_length=MAX_LENGTH_UNIT
    )

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name_plural = 'Ингредиенты'
        verbose_name = 'Ингредиент'

    def __str__(self):
        return self.name[:LENGTH_HEADER]


class Tag(models.Model):
    """
    Тег для рецепта.
    Все поля обязательны для заполнения и уникальны.
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH_TAG,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет в формате HEX-кода',
        help_text='Цветовой HEX-код (например, #49B64E)',
        max_length=MAX_LENGTH_HEX,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='slug - идентификатор',
        max_length=MAX_LENGTH_SLUG,
        unique=True
    )

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name_plural = 'Теги'
        verbose_name = 'Тег'

    def __str__(self):
        return self.name[:LENGTH_HEADER]


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
        upload_to='recipes/%Y/%m/%d',
        blank=True
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
        help_text='Добавьте описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipe_ingredient',
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe_tag',
        verbose_name='Тег',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах',
    )

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name_plural = 'Рецепты'
        verbose_name = 'Рецепт'

    def __str__(self):
        return self.name[:LENGTH_HEADER]

    def get_ingredient(self):
        return ', '.join(
            [str(field) for field in self.ingredients.all()]
            )

    def get_tag(self):
        return ', '.join(
            [str(field) for field in self.tags.all()]
            )


class RecipeIngredient(models.Model):
    """
    Промежуточная модель.
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
        decimal_places=MAX_DECIMAL_PLACES
    )
