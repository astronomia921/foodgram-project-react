from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from users.models import Follow

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)

User = get_user_model()


class RecipeAPITestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            email="vpupkin@yandex.ru",
            username="vasya.pupkin",
            first_name="Вася",
            last_name="Пупкин",
            password="12331214ssad"
        )
        self.user_2 = User.objects.create_user(
            email="test@yandex.ru",
            username="testuser",
            first_name="testname",
            last_name="testlast",
            password="12314ssad"
        )
        self.user_3 = User.objects.create_user(
            email="test3@yandex.ru",
            username="testuser3",
            first_name="testname3",
            last_name="testlast3",
            password="12314ssad"
        )
        self.is_subscribed = Follow.objects.filter(
            user=self.user_1, author=self.user_2).exists()
        self.recipe_1 = Recipe.objects.create(
            author=self.user_2,
            name="Блюда№1",
            image=None,
            text='текст блюда',
            cooking_time=2
        )
        self.ingredient = Ingredient.objects.create(
            name="Капуста",
            measurement_unit="кг",
        )
        self.tag = Tag.objects.create(
            name='Завтрак',
            color='#E26C2D',
            slug='breakfast',
        )
        self.recipe_1.ingredients.add(self.ingredient)
        self.recipe_1.tags.add(self.tag)
        self.recipe_ingredient, _ = RecipeIngredient.objects.get_or_create(
            recipe=self.recipe_1,
            ingredient=self.ingredient,
            defaults={'amount': 2},
        )
        self.favorited = Favorite.objects.create(
            user=self.user_1,
            recipe=self.recipe_1
        )
        self.in_shopping_cart = ShoppingCart.objects.create(
            user=self.user_1,
            recipe=self.recipe_1
        )
        self.is_favorited = Favorite.objects.filter(
            user=self.user_1, recipe=self.recipe_1).exists()
        self.is_in_shopping_cart = ShoppingCart.objects.filter(
            user=self.user_1, recipe=self.recipe_1).exists()

        self.client = APIClient()
        self.client_1 = APIClient()
        self.client_2 = APIClient()
        self.client_3 = APIClient()
        self.client.force_authenticate(user=self.user_1)
        self.client_1.force_authenticate(user=self.user_3)
        self.client_3.force_authenticate(user=self.user_2)

    def test_recipe_list(self):
        response = self.client.get('/api/recipes/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(len(response.json()['results']), 1)
        self.assertDictContainsSubset({
            "id": self.recipe_1.id,
            "tags": [
                {
                    "id": self.tag.id,
                    "name": self.tag.name,
                    "color": self.tag.color,
                    "slug": self.tag.slug
                }
            ],
            "author": {
                "email": self.user_2.email,
                "id": self.user_2.id,
                "username": self.user_2.username,
                "first_name": self.user_2.first_name,
                "last_name": self.user_2.last_name,
                "is_subscribed": self.is_subscribed
            },
            "ingredients": [
                {
                    "id": self.ingredient.id,
                    "name": self.ingredient.name,
                    "measurement_unit": self.ingredient.measurement_unit,
                    "amount": self.recipe_ingredient.amount
                }
            ],
            "is_favorited": self.is_favorited,
            "is_in_shopping_cart": self.is_in_shopping_cart,
            "name": self.recipe_1.name,
            "image": self.recipe_1.image,
            "text": self.recipe_1.text,
            "cooking_time": self.recipe_1.cooking_time
        }, response.json()['results'][0]
        )

    def test_recipe_by_id(self):
        response = self.client.get('/api/recipes/1/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        expectation = {
            "id": 1,
            "tags": [
                {
                    "id": 1,
                    "name": "Завтрак",
                    "color": "#E26C2D",
                    "slug": "breakfast"
                }
            ],
            "author": {
                "email": "test@yandex.ru",
                "id": 2,
                "username": "testuser",
                "first_name": "testname",
                "last_name": "testlast",
                "is_subscribed": False
            },
            "ingredients": [
                {
                    "id": 1,
                    "name": "Капуста",
                    "measurement_unit": "кг",
                    "amount": 1
                }
            ],
            "is_favorited": True,
            "is_in_shopping_cart": True,
            "name": "Блюда№1",
            "image": None,
            "text": "текст блюда",
            "cooking_time": 2
        }
        self.assertDictContainsSubset(expectation, response.data)

    def test_create_recipe(self):
        payload = {
            "ingredients": [
                {
                    "id": 1,
                    "amount": 2
                }
            ],
            "tags": [
                1,
            ],
            "image": None,
            "name": "Блюда№2",
            "text": "текст блюда",
            "cooking_time": 2
        }
        response = self.client.post('/api/recipes/', payload, format="json")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        response_2 = self.client_2.post('/api/recipes/',
                                        payload, format="json")
        self.assertEqual(response_2.status_code, HTTPStatus.UNAUTHORIZED)

        payload_not_valid = {
            "ingredients": [
                {
                    "id": 1,
                }
            ],
            "tags": [
                1,
            ],
            "image": None,
            "name": "Блюда№2",
            "text": "текст блюда",
            "cooking_time": 2
        }
        response_3 = self.client.post('/api/recipes/',
                                      payload_not_valid, format="json")
        self.assertEqual(response_3.status_code, HTTPStatus.BAD_REQUEST)

        payload_not_found = {
            "ingredients": [
                {
                    "id": 3,  # not found
                    "amount": 2
                }
            ],
            "tags": [
                1,
            ],
            "image": None,
            "name": "Блюда№2",
            "text": "текст блюда",
            "cooking_time": 2
        }
        response_4 = self.client.post('/api/recipes/',
                                      payload_not_found, format="json")
        self.assertEqual(response_4.status_code, HTTPStatus.NOT_FOUND)

    def test_update_recipe(self):
        payload = {
            "ingredients": [
                {
                    "id": 1,
                    "amount": 2
                }
            ],
            "tags": [
                1,
            ],
            "image": None,
            "name": "Блюда№2",
            "text": "текст блюда",
            "cooking_time": 2
        }
        response = self.client.post('/api/recipes/', payload, format="json")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        payload_update = {
            "ingredients": [
                {
                    "id": 1,
                    "amount": 4  # update
                }
            ],
            "tags": [
                1,
            ],
            "image": None,
            "name": "Блюда№2",
            "text": "текст блюда",
            "cooking_time": 2
        }
        response_2 = self.client.patch('/api/recipes/2/',
                                       payload_update, format="json")
        self.assertEqual(response_2.status_code, HTTPStatus.OK)
        response_3 = self.client_2.patch('/api/recipes/2/',
                                         payload_update, format="json")
        self.assertEqual(response_3.status_code, HTTPStatus.UNAUTHORIZED)
        response_4 = self.client.patch('/api/recipes/5/',
                                       payload_update, format="json")
        self.assertEqual(response_4.status_code, HTTPStatus.NOT_FOUND)
        response_5 = self.client_1.patch('/api/recipes/2/',
                                         payload_update, format="json")
        self.assertEqual(response_5.status_code, HTTPStatus.FORBIDDEN)

    def test_delete_recipe(self):
        response_1 = self.client.delete('/api/recipes/1/', format="json")
        self.assertEqual(response_1.status_code, HTTPStatus.FORBIDDEN)
        response_2 = self.client_2.delete('/api/recipes/1/', format="json")
        self.assertEqual(response_2.status_code, HTTPStatus.UNAUTHORIZED)
        response_3 = self.client.delete('/api/recipes/5/', format="json")
        self.assertEqual(response_3.status_code, HTTPStatus.NOT_FOUND)
        response_4 = self.client_3.delete('/api/recipes/1/', format="json")
        self.assertEqual(response_4.status_code, HTTPStatus.NO_CONTENT)


class ShoppingCartFavoriteAPITestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            email="vpupkin@yandex.ru",
            username="vasya.pupkin",
            first_name="Вася",
            last_name="Пупкин",
            password="12331214ssad"
        )
        self.recipe_1 = Recipe.objects.create(
            author=self.user_1,
            name="Блюда№1",
            image=None,
            text='текст блюда',
            cooking_time=2
        )
        self.client = APIClient()
        self.client_2 = APIClient()
        self.client.force_authenticate(user=self.user_1)

    def test_download_shopping_cart(self):
        url = '/api/recipes/download_shopping_cart/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response_2 = self.client_2.get(url)
        self.assertEqual(response_2.status_code, HTTPStatus.UNAUTHORIZED)

    def test_add_shopping_cart(self):
        url = '/api/recipes/1/shopping_cart/'
        data = {
            "id": 1,
            "name": "Блюда№1",
            "image": None,
            "cooking_time": 2
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        user_data = response.json()
        recipe_count_2 = ShoppingCart.objects.filter(
            user=self.user_1).count()
        self.assertEqual(recipe_count_2, 1)
        for key in user_data:
            self.assertEqual(response.json()[key], user_data[key])
        response_2 = self.client_2.post(url, data, format="json")
        self.assertEqual(response_2.status_code, HTTPStatus.UNAUTHORIZED)
        response_3 = self.client.post(url, data, format="json")
        self.assertEqual(response_3.status_code, HTTPStatus.BAD_REQUEST)

    def test_del_shopping_cart(self):
        url = '/api/recipes/1/shopping_cart/'
        data = {
            "id": 1,
            "name": "Блюда№1",
            "image": None,
            "cooking_time": 2
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        response_1 = self.client_2.delete(url, format="json")
        self.assertEqual(response_1.status_code, HTTPStatus.UNAUTHORIZED)
        response_2 = self.client.delete(url, format="json")
        self.assertEqual(response_2.status_code, HTTPStatus.NO_CONTENT)
        url_2 = '/api/recipes/10/shopping_cart/'
        response_3 = self.client.delete(url_2, format="json")
        self.assertEqual(response_3.status_code, HTTPStatus.NOT_FOUND)

    def test_add_favorite(self):
        url = '/api/recipes/1/favorite/'
        data = {
            "id": 1,
            "name": "Блюда№1",
            "image": None,
            "cooking_time": 2
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        response_1 = self.client_2.post(url, data, format="json")
        self.assertEqual(response_1.status_code, HTTPStatus.UNAUTHORIZED)
        response_2 = self.client.post(url, data, format="json")
        self.assertEqual(response_2.status_code, HTTPStatus.BAD_REQUEST)

    def test_del_favorite(self):
        url = '/api/recipes/1/favorite/'
        data = {
            "id": 1,
            "name": "Блюда№1",
            "image": None,
            "cooking_time": 2
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        response_1 = self.client_2.delete(url, format="json")
        self.assertEqual(response_1.status_code, HTTPStatus.UNAUTHORIZED)
        response_2 = self.client.delete(url, format="json")
        self.assertEqual(response_2.status_code, HTTPStatus.NO_CONTENT)
        response_2 = self.client.delete(url, data, format="json")
        self.assertEqual(response_2.status_code, HTTPStatus.BAD_REQUEST)
