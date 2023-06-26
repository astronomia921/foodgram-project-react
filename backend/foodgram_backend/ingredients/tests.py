from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Ingredient

User = get_user_model()


class IngredientAPITestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user_1 = User.objects.create_user(
            email="vpupkin@yandex.ru",
            username="vasya.pupkin",
            first_name="Вася",
            last_name="Пупкин",
            password="12331214ssad"
        )
        self.ingredient = Ingredient.objects.create(
            name="Капуста",
            measurement_unit="кг"
        )
        self.ingredient_2 = Ingredient.objects.create(
            name="Картошка",
            measurement_unit="кг"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_1)

    def test_get_ingredients_list(self):
        response = self.client.get('/api/ingredients/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(len(response.json()['results']), 2)
        self.assertDictContainsSubset(
            {
                "name": self.ingredient.name,
                "measurement_unit": self.ingredient.measurement_unit,
            }, response.json()['results'][0]
        )

    def test_get_ingredients_by_id(self):
        response = self.client.get('/api/ingredients/1/')
        response_2 = self.client.get('/api/ingredients/3/')
        expectation = {
            "id": 1,
            "name": "Капуста",
            "measurement_unit": "кг"
        }
        self.assertEqual(response.data, expectation)
        self.assertEqual(response_2.status_code, HTTPStatus.NOT_FOUND)
