from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAG_URL = reverse('recipe:tag-list')

def detail_url(tag_url):
    return reverse('recipe:tag-detail', args=[tag_url.name])

def create_user(email='user@example.com', password='testpass'):
    return get_user_model().objects.create_user(email, password)

class PublicTagsApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(TAG_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTest(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        response = self.client.get(TAG_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_user(self):
        user2 = create_user(email = 'user2@example.com')
        Tag.objects.create(user=user2, name='Fruit')
        tags = Tag.objects.create(user=self.user, name= 'comfort_food')

        response = self.client.get(TAG_URL)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], tags.name)
        self.assertEqual(response.data[0]['id',tags.id])


    def test_update_tag(self):
        tag = Tag.objects.create(user=self.user, name='Vegetarian')
        payload =   {'name': 'Vegetarian'}
        url = detail_url(tag.id)
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name,payload['name'])


    def test_delete_tag(self):
        tag = Tag.objects.create(user= self.user, name= 'Breakfast')

        url = detail_url(tag.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(use= self.user)
        self.assertFalse(tags.exists())




