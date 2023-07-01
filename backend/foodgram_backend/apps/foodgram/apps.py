from django.apps import AppConfig


class FoodgramConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    label = 'foodgram'
    name = 'apps.foodgram'
    verbose_name = 'Кулинарный помощник'
