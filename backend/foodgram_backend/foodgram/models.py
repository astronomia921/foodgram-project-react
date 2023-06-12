from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    """
    Ингредиенты.
    """
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        help_text='Единицы измерения: шт, ложки, стакан, кг, щепотка',
        max_length=50
    )

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name_plural = 'Ингредиенты'
        verbose_name = 'Ингредиент'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Тег для рецепта.
    Все поля обязательны для заполнения и уникальны.
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=50,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет в формате HEX-кода',
        help_text='Цветовой HEX-код (например, #49B64E)',
        max_length=7,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='slug - идентификатор',
        max_length=50,
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
        return self.name


class Recipe(models.Model):
    """
    Рецепт блюда.
    Все поля обязательны.
    """
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        help_text='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='food_recipe'
    )
    name = models.CharField(
        max_length=200,
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
        return self.name

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
        max_digits=6,
        decimal_places=2
    )
