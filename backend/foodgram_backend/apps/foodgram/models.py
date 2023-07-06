from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from foodgram_backend.settings import LENGTH_HEADER, MAX_LENGTH_NAME

from apps.ingredients.models import Ingredient
from apps.tags.models import Tag


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
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
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
        default_related_name = 'recipe_obj'

    def __str__(self):
        return self.name[:LENGTH_HEADER]


class RecipeIngredient(models.Model):
    """
    Модель для ингредиентов рецепта.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipe',
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, 'Колличество ингредиента в рецепте должно быть >= 1.'
            )
        ],
        default=1
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.recipe.name}: {self.ingredient.name} {self.amount}'


class RecipeTags(models.Model):
    """
    Модель для тегов рецепта.
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
        default_related_name = 'recipe_tag'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_tag'
            )
        ]

    def __str__(self):
        return f"У рецепта {self.recipe} есть тег {self.tag}"


class Favorite(models.Model):
    """
    Модель избранных рецептов.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='in_favorite',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ['recipe']
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_favorite',
            ),
        )

    def __str__(self):
        return (f"Рецепт: '{self.recipe}' добавлен в избранное"
                f"пользователем: '{self.user.username}'")


class ShoppingCart(models.Model):
    """
    Модель корзины покупок.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shopping_recipe'
    )

    class Meta:
        verbose_name = 'Cписок покупок'
        verbose_name_plural = 'Список покупок'

        ordering = ['recipe']
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='shopping_recipe_user',
            ),
        )

    def __str__(self):
        return (f"Рецепт: '{self.recipe}' добавлен в список покупок"
                f"пользователю: '{self.user.username}'")
