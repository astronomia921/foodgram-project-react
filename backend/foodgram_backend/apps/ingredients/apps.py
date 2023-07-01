from django.apps import AppConfig


class IngredientsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    label = 'ingredients'
    name = 'apps.ingredients'
    verbose_name = 'Ингредиенты'
