from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


URL_SIGNUP = reverse('auth:create')
URL_TOKEN = reverse('auth:token')


class TestPublicUsersApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='user_test@gmail.com',
            password='secret@123',
            first_name='usuario de test'
        )

    def test_method_not_allow(self):
        """Verificar que sólo se permite el método POST"""
        res = self.client.get(URL_SIGNUP)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        res = self.client.put(URL_SIGNUP)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        res = self.client.patch(URL_SIGNUP)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        res = self.client.delete(URL_SIGNUP)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_new_user(self):
        """Testear la creación de un nuevo usuario"""
        payload = {
            'email': 'test@gmail.com',
            'first_name': 'testing1',
            'password': 'password123',
            'password_confirmation': 'password123',
        }

        res = self.client.post(URL_SIGNUP, payload)
        user = get_user_model().objects.get(email=payload['email'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['email'], payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_password_confirmation(self):
        """Testear la confirmación del password"""
        payload_fail = {
            'email': 'test@gmail.com',
            'first_name': 'testing1',
            'password': 'password123',
            'password_confirmation': 'password12',
        }

        res = self.client.post(URL_SIGNUP, payload_fail)

        exists_user = get_user_model().objects.filter(
            email=payload_fail['email']
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(exists_user)

    def test_obtain_token(self):
        """Verificar el obtener token"""
        payload = {
            'email': 'user_test@gmail.com',
            'password': 'secret@123',
        }
        res = self.client.post(URL_TOKEN, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
