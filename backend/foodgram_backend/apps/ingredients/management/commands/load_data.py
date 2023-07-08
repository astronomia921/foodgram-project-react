import json

from django.core.management.base import BaseCommand

from apps.ingredients.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка данных из JSON файла в таблицу Ingredients'

    def handle(self, *args, **options):
        file_path = '/app/data/ingredients.json'
        with open(file_path, encoding="utf8") as f:
            data = json.load(f)
            for item in data:
                Ingredient.objects.get_or_create(
                    name=item['name'],
                    measurement_unit=item['measurement_unit']
                )
        self.stdout.write(
            self.style.SUCCESS('Загрузка данных прошла успешно.'))
