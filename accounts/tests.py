import os
import django
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from accounts.models import RequestCount
from rest_framework_simplejwt.tokens import RefreshToken

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
os.environ['DJANGO_ENV'] = 'test'

django.setup()

User = get_user_model()


class RegisterUserAPIViewTests(APITestCase):

    def setUp(self):
        self.url = '/register/'
        self.payload = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        self.existing_user = User.objects.create_user(
            username='existinguser', password='password123')

    def test_register_user_success(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)

    def test_existing_user(self):
        payload = {
            'username': 'existinguser',
            'password': 'newpassword123'
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'],
                         "User with this username already exists!")

    def test_missing_username(self):
        payload = {
            'password': 'testpassword123'
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_missing_password(self):
        payload = {
            'username': 'newuser'
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)


class RequestCountViewTests(APITestCase):

    def setUp(self):
        self.url = '/request-count/'
        self.reset_url = '/request-count/reset/'
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        RequestCount.objects.create(count=0)

    def test_get_count(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['requests'], 1)

    def test_count_increments(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['requests'], 1)
        response = self.client.get(self.url)
        self.assertEqual(response.data['requests'], 2)

    def test_reset_count(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['requests'], 1)

        reset_response = self.client.post(self.reset_url)
        self.assertEqual(reset_response.status_code, status.HTTP_200_OK)
        self.assertEqual(reset_response.data['message'],
                         'Request count reset successfully.')
