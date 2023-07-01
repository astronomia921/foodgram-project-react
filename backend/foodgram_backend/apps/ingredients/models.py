from django.db import models

from foodgram_backend.settings import (LENGTH_HEADER, MAX_LENGTH_NAME,
                                       MAX_LENGTH_UNIT)


class Ingredient(models.Model):
    """
    Ингредиенты блюда (ништяки).
    """
    name = models.CharField(
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента',
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
