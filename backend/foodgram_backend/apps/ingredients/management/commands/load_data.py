import json

from django.core.management.base import BaseCommand

from apps.ingredients.models import Ingredient

from foodgram_backend.settings import FILE_PATH


class Command(BaseCommand):
    help = 'Загрузка данных из JSON файла в таблицу Ingredients'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Путь до JSON файла')

    def handle(self, *args, **options):
        file_path = options['path'] + 'ingredients.json'
        with open(file_path, encoding="utf8") as f:
            data = json.load(f)
            for item in data:
                Ingredient.objects.create(
                    name=item['name'],
                    measurement_unit=item['measurement_unit']
                )
        self.stdout.write(
            self.style.SUCCESS('Загрузка данных прошла успешно.'))
