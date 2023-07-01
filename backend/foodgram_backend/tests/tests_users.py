from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from apps.foodgram.models import Recipe, RecipeIngredient
from apps.ingredients.models import Ingredient
from apps.tags.models import Tag

from users.models import Follow

User = get_user_model()


class UserCreateAPITestCase(TestCase):
    def test_create_user(self):
        client = APIClient()
        url = "/api/users/"
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "12331214ssad"
        }
        response = client.post("/api/users/", data, format="json")
        for key in data:
            if key != 'password':
                self.assertEqual(response.json()[key], data[key])
                self.assertEqual(getattr(User.objects.get(), key), data[key])
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        data_invalid_email = {
            "email": "vpupkin@yandex",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "Qwerty123"
        }
        response = self.client.post(url, data_invalid_email, format="json")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        data_invalid_username = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya_pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "Qwerty123"
        }
        response = self.client.post(url, data_invalid_username, format="json")
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)


class UserAPITestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            email="vpupkin@yandex.ru",
            username="vasya.pupkin",
            first_name="Вася",
            last_name="Пупкин",
            password="12331214ssad"
        )
        self.user_2 = User.objects.create_user(
            email="dmitry_zavorotnii@yandex.ru",
            username="Dmitry",
            first_name="Dmitry",
            last_name="Zavorotny",
            password="12314ssad"
        )
        self.user_3 = User.objects.create_user(
            email="alan@yandex.ru",
            username="Allen",
            first_name="Allen",
            last_name="Dulles",
            password="12314s22sad"
        )
        self.client = APIClient()
        self.client_2 = APIClient()
        self.client.force_authenticate(user=self.user_1)

    def test_get_users_list(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(len(response.json()['results']), 3)
        self.assertDictContainsSubset(
            {
                'email': self.user_3.email,
                'id': self.user_3.id,
                'username': self.user_3.username,
                'first_name': self.user_3.first_name,
                'last_name': self.user_3.last_name,
                'is_subscribed': False
            }, response.json()['results'][0]
        )

    def test_get_user_by_me_id(self):
        response_1 = self.client.get('/api/users/me/')
        response_2 = self.client.get('/api/users/1/')
        response_3 = self.client_2.get('/api/users/2/')
        response_4 = self.client.get('/api/users/4/')
        response_5 = self.client_2.get('/api/users/me/')
        expectation = {
            "email": "vpupkin@yandex.ru",
            "id": 1,
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "is_subscribed": False
        }
        self.assertEqual(response_1.data, expectation)
        self.assertEqual(response_2.data, expectation)

        self.assertEqual(response_3.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response_4.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response_5.status_code, HTTPStatus.UNAUTHORIZED)

    def test_set_password(self):
        url = '/api/users/set_password/'
        data_1 = {
            "new_password": "ssad12331214",
            "current_password": "12331214ssad"
        }
        data_2 = {
            "new_password": "ssad12331214",
        }
        response_1 = self.client.post(url, data_1, format="json")
        response_2 = self.client.post(url, data_2, format="json")
        response_3 = self.client_2.post(url, data_1, format="json")
        self.assertEqual(response_1.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(response_2.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response_3.status_code, HTTPStatus.UNAUTHORIZED)

    def test_get_token(self):
        url = '/api/auth/token/login/'
        data = {
            "password": "12331214ssad",
            "email": "vpupkin@yandex.ru"
        }
        response_1 = self.client_2.post(url, data, format="json")
        self.assertEqual(response_1.status_code, HTTPStatus.OK)

    def test_delete_token(self):
        url = '/api/auth/token/logout/'
        data = {
            "password": "12331214ssad",
            "email": "vpupkin@yandex.ru"
        }
        response_1 = self.client.post(url, data, format="json")
        self.assertEqual(response_1.status_code, HTTPStatus.NO_CONTENT)
        self.client.logout()
        response_2 = self.client.post(url, data, format="json")
        self.assertEqual(response_2.status_code, HTTPStatus.UNAUTHORIZED)


class FollowAPITestCase(TestCase):
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
            email="alan@yandex.ru",
            username="Allen",
            first_name="Allen",
            last_name="Dulles",
            password="12314s22sad"
        )
        self.follow = Follow.objects.create(
            user=self.user_1,
            author=self.user_2
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
        self.recipe_1 = Recipe.objects.create(
            author=self.user_1,
            name="Блюда№1",
            image=None,
            text='текст блюда',
            cooking_time=2
        )
        self.recipe_2 = Recipe.objects.create(
            author=self.user_2,
            name="Блюда№2",
            image=None,
            text='текст блюда',
            cooking_time=3
        )
        self.recipe_3 = Recipe.objects.create(
            author=self.user_3,
            name="Блюда№3",
            image=None,
            text='текст блюда',
            cooking_time=4
        )
        self.recipe_1.ingredients.add(self.ingredient)
        self.recipe_1.tags.add(self.tag)
        self.recipe_2.ingredients.add(self.ingredient)
        self.recipe_2.tags.add(self.tag)
        self.recipe_ingredient = RecipeIngredient.objects.get_or_create(
            recipe=self.recipe_1,
            ingredient=self.ingredient,
            amount=2,
        )
        self.recipe_count = Recipe.objects.filter(author=self.user_2).count()
        self.is_subscribed = Follow.objects.filter(
            user=self.user_1, author=self.user_2).exists()
        self.client = APIClient()
        self.client_2 = APIClient()
        self.client.force_authenticate(user=self.user_1)

    def test_subscribe(self):
        url = '/api/users/3/subscribe/'
        response_1 = self.client.post(url, format="json")
        self.assertEqual(response_1.status_code, HTTPStatus.CREATED)
        user_data = response_1.json()
        for key in user_data:
            self.assertEqual(response_1.json()[key], user_data[key])

        recipe_data_1 = user_data['recipes'][0]
        self.assertEqual(recipe_data_1['id'], self.recipe_3.id)
        self.assertEqual(recipe_data_1['name'], self.recipe_3.name)
        self.assertEqual(recipe_data_1['image'], None)
        self.assertEqual(
            recipe_data_1['cooking_time'], self.recipe_3.cooking_time)

        response_2 = self.client_2.post(url, format="json")
        self.assertEqual(response_2.status_code, HTTPStatus.UNAUTHORIZED)

        url_3 = '/api/users/4/subscribe/'
        response_3 = self.client.post(url_3, format="json")
        self.assertEqual(response_3.status_code, HTTPStatus.NOT_FOUND)

        url_self = '/api/users/1/subscribe/'
        response_self = self.client.post(url_self, format="json")
        self.assertEqual(response_self.status_code, HTTPStatus.BAD_REQUEST)

        url_del = '/api/users/3/subscribe/'
        response_del = self.client.delete(url_del, format="json")
        self.assertEqual(response_del.status_code, HTTPStatus.NO_CONTENT)

        url_del_2 = '/api/users/4/subscribe/'
        response_del_2 = self.client.delete(url_del_2, format="json")
        self.assertEqual(response_del_2.status_code, HTTPStatus.NOT_FOUND)

        url_del_3 = '/api/users/3/subscribe/'
        response_del_3 = self.client_2.delete(url_del_3, format="json")
        self.assertEqual(response_del_3.status_code, HTTPStatus.UNAUTHORIZED)

    def test_subscriptions(self):
        response = self.client.get('/api/users/subscriptions/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(len(response.json()['results']), 1)
        self.assertDictContainsSubset(
            {
                'email': self.user_2.email,
                'id': self.user_2.id,
                'username': self.user_2.username,
                'first_name': self.user_2.first_name,
                'last_name': self.user_2.last_name,
                'is_subscribed': self.is_subscribed,
                "recipes": [
                    {
                        "id": self.recipe_2.id,
                        "name": self.recipe_2.name,
                        "image": self.recipe_2.image,
                        "cooking_time": self.recipe_2.cooking_time
                    }
                ],
                "recipes_count": self.recipe_count
            }, response.json()['results'][0]
        )
        response = self.client_2.get('/api/users/subscriptions/')
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
