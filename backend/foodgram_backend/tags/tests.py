from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Tag

User = get_user_model()


class TagAPITestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user_1 = User.objects.create_user(
            email="vpupkin@yandex.ru",
            username="vasya.pupkin",
            first_name="Вася",
            last_name="Пупкин",
            password="12331214ssad"
            )
        self.tags = Tag.objects.create(
            name='Завтрак',
            color='#E26C2D',
            slug='breakfast',
        )
        self.tags_2 = Tag.objects.create(
            name='Обед',
            color='#7FFF00',
            slug='lunch',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_1)

    def test_get_tags_list(self):
        response = self.client.get('/api/tags/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(len(response.json()['results']), 2)
        self.assertDictContainsSubset(
            {
                "name":  self.tags.name,
                "color": self.tags.color,
                "slug":  self.tags.slug
                },  response.json()['results'][0]
            )

    def test_get_tags_by_id(self):
        response = self.client.get('/api/tags/1/')
        response_2 = self.client.get('/api/tags/3/')
        expectation = {
            "id": 1,
            "name": "Завтрак",
            "color": "#E26C2D",
            "slug": "breakfast"
            }
        self.assertEqual(response.data, expectation)
        self.assertEqual(response_2.status_code, HTTPStatus.NOT_FOUND)
