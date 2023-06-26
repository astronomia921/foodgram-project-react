from django.core.validators import RegexValidator
from django.db import models

from foodgram_backend.settings import (LENGTH_HEADER, MAX_LENGTH_HEX,
                                       MAX_LENGTH_SLUG, MAX_LENGTH_TAG,
                                       REGEX_VALIDATORS)


class Tag(models.Model):
    """
    Тег для рецепта.
    Все поля обязательны для заполнения и уникальны.
    """
    name = models.CharField(
        verbose_name='Название тега',
        help_text='Введите название тега',
        max_length=MAX_LENGTH_TAG,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет в формате HEX-кода',
        help_text='Цветовой HEX-код (например, #49B64E)',
        max_length=MAX_LENGTH_HEX,
        unique=True,
        validators=[
            RegexValidator(
                regex=REGEX_VALIDATORS,
                message='Введите значение цвета в формате HEX! Пример:#FF0000'
            )
        ]
    )
    slug = models.SlugField(
        verbose_name='Slug - идентификатор',
        help_text='Введите slug - идентификатор',
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
