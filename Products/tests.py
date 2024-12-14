import json
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
import base64
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient, APITestCase
from Products.models import Nike, User
from Products.serializers import NikeSerializer, RegisterSerializer, LoginSerializer, LogoutSerializer
from Products.factories import NikeFactory, UserFactory
from django.core.files.uploadedfile import SimpleUploadedFile

class NikeListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.nike = NikeFactory()

    def test_get_nike(self):
        response = self.client.get('/api/nike/')
        nike = Nike.objects.all()
        serializer = NikeSerializer(nike, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_post_nike(self):
        url = '/api/nike/'
        nike_factory_instance = NikeFactory.build()
        image_path = "/home/naitik/Projects/Django-reactapp/BackendProducts/Products/test_image.jpg"
        with open(image_path, "rb") as image_file:
            image_binary_data = image_file.read()
        image_base64 = base64.b64encode(image_binary_data).decode('utf-8')
        nike_factory_data = {
            'ShoeName': nike_factory_instance.ShoeName,
            'ShoeNumber': nike_factory_instance.ShoeNumber,
            'ShoeType': nike_factory_instance.ShoeType,
            'Gender': nike_factory_instance.Gender,
            'Price': nike_factory_instance.Price,
            'images': image_base64,
        }
        response = self.client.post(url, nike_factory_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Nike.objects.count(), 2)


class NikeDetailsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.nike = NikeFactory()

    def test_get_object(self):
        response = self.client.get(f'/api/nike/{self.nike.id}/')
        serializer = NikeSerializer(self.nike)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_put_nike(self):
        data = {
            'ShoeName': 'Updated Name',
            'ShoeNumber': 7,
            'ShoeType': 'Updated ShoeType',
            'Gender': 'Updated Gender',
            'Price': 4599,
            'images': '',
        }
        response = self.client.put(f'/api/nike/{self.nike.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)


    def test_delete_nike(self):
        response = self.client.delete(f'/api/nike/{self.nike.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Nike.objects.count(), 0)

class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post('/api/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        user = UserFactory(username='testuser', password='testpassword')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post('/api/login/',data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        user = UserFactory()
        refresh_token = user.tokens()['refresh']
        data = {
            'refresh': str(refresh_token)
        }
        response = self.client.post('/api/logout/', data=data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED,(response.status_code, response.content))