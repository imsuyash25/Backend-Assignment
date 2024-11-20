import os
import django
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from movies.models import Collection, Movie
from rest_framework_simplejwt.tokens import RefreshToken

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
os.environ['DJANGO_ENV'] = 'test'

django.setup()

User = get_user_model()


class MoviesListTestCases(APITestCase):
    '''
        Unit test to test endpoints of List Movies
    '''
    def setUp(self):
        self.user = User.objects.create_user(
                        username='testuser', password='testpass')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.url = reverse('movie-list')

    @patch('requests.Session.get')
    def test_list_movies_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'results': [],
            'next': None,
            'previous': None
        }

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_list_movies_unauthorized(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('requests.Session.get')
    def test_list_movies_error(self, mock_get):
        mock_get.return_value.status_code = 500
        mock_get.return_value.text = 'Internal Server Error'

        response = self.client.get(self.url)
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('Error', response.data)


class CollectionListCreateTests(APITestCase):
    '''
        Unit test to test List and Create Endpoints of Collection
    '''
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.url = '/collection/'

    def test_create_collection_success(self):
        data = {
            "title": "Test Collection",
            "description": "description",
            "movies": [
                {
                    "title": "Test Movie 1",
                    "description": "description",
                    "genres": "comedy",
                    "uuid": "123e4567-e89b-12d3-a456-426614170000"
                },
                {
                    "title": "Test Movie 2",
                    "description": "description",
                    "genres": "action",
                    "uuid": "123e4567-e89b-12d3-a456-426614171111"
                }]
            }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('collection_uuid', response.data)

    def test_get_collections_success(self):
        collec1 = Collection.objects.create(title="Test Collection1",
                                            description="description1",
                                            user=self.user)
        collec2 = Collection.objects.create(title="Test Collection2",
                                            description="description2",
                                            user=self.user)

        response = self.client.get('/collection/')
        response_collection = response.data["data"]['collections']

        self.assertEqual(response.data["is_success"], True)
        self.assertEqual(len(response_collection), 2)
        self.assertEqual(response_collection[0]['uuid'], str(collec1.uuid))
        self.assertEqual(response_collection[0]['title'], collec1.title)
        self.assertEqual(response_collection[1]['uuid'], str(collec2.uuid))
        self.assertEqual(response_collection[1]['title'], collec2.title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('favourite_genres', response.data['data'])

    def test_create_collection_unauthorized(self):
        self.client.credentials()
        data = {
            "title": "Test Collection",
            "description": "description",
            "movies": [
                {
                    "title": "Test Movie 1",
                    "description": "description",
                    "genres": "comedy",
                    "uuid": "123e4567-e89b-12d3-a456-426614170000"
                },
                {
                    "title": "Test Movie 2",
                    "description": "description",
                    "genres": "action",
                    "uuid": "123e4567-e89b-12d3-a456-426614171111"
                }]
            }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_collection_invalid_data(self):
        data = {'name': ''}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CollectionManageViewTests(APITestCase):
    '''
        Unit test to test Retrieve, Update, Destroy \
        Endpoints of Collection and Movies
    '''
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.collection = Collection.objects.create(
            title='My Collection',
            description='Collection Description',
            user=self.user)
        self.movie = Movie.objects.create(
            collection=self.collection,
            title='Test Movie',
            description='An unsuccessful sculptor',
            genres="Horror,Mystery,Thriller",
            uuid='388c99da-0cba-4ff0-a528-faea153b43c3'
        )
        self.url = f'/collection/{self.collection.uuid}/'

    def test_retrieve_collection_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data["title"], self.collection.title)
        self.assertEqual(response.data["description"],
                         self.collection.description)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('movies', response.data)

    def test_update_collection_success(self):
        data = {
            "title": "Test Collection Updated",
            "description": "Updated",
            "movies": [
                {
                    "title": "Mission Impossible",
                    "description": "Description",
                    "genres": "comedy",
                    "uuid": "123e4567-e89b-12d3-a456-426614170001"
                }
            ]
            }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.collection.refresh_from_db()
        self.assertEqual(self.collection.title, data['title'])
        self.assertEqual(self.collection.description, data['description'])
        self.assertIn('movies', response.data)

    def test_delete_collection_success(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Collection.objects.filter(
            uuid=self.collection.uuid).exists())

    def test_collection_manage_unauthorized(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
