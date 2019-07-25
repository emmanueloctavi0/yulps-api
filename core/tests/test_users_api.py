from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


URL_SIGNUP = reverse('auth:create')
URL_TOKEN = reverse('auth:token')
URL_ME = reverse('auth:me')


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

    def test_email_is_unique(self):
        """Test para confirmar que no se crean
        dos usuario con el mismo email
        """
        payload = {
            'email': 'user_test@gmail.com',
            'first_name': 'testing1',
            'password': 'password123',
            'password_confirmation': 'password123',
        }

        res = self.client.post(URL_SIGNUP, payload)
        user_exists = get_user_model().objects.filter(
            first_name=payload['first_name']
        ).exists()

        self.assertFalse(user_exists)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_password_confirmation_is_empty(self):
        """Test si no se manda el password confirmation"""

        payload_fail = {
            'email': 'test@gmail.com',
            'first_name': 'testing1',
            'password': 'password123',
        }

        res = self.client.post(URL_SIGNUP, payload_fail)

        exists_user = get_user_model().objects.filter(
            email=payload_fail['email']
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(exists_user)

    def test_password_is_empty(self):
        """Test si no se manda el password, sólo el password confirmation"""

        payload_fail = {
            'email': 'test@gmail.com',
            'first_name': 'testing1',
            'password_confirmation': 'password123',
        }

        res = self.client.post(URL_SIGNUP, payload_fail)

        exists_user = get_user_model().objects.filter(
            email=payload_fail['email']
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(exists_user)

    def test_dont_send_password(self):
        """Test si no se manda ningún password"""

        payload_fail = {
            'email': 'test@gmail.com',
            'first_name': 'testing1',
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
        self.assertIn('token', res.data)


class TestPrivateUserApi(TestCase):
    """Test para usuarios autenticados"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            first_name='testing1',
            last_name='last_name_test',
            password='password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_user_info_retrieved(self):
        """Testear que la información del usuario logueado es correcta"""
        res = self.client.get(URL_ME)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], self.user.email)
        self.assertEqual(res.data['first_name'], self.user.first_name)
        self.assertEqual(res.data['last_name'], self.user.last_name)
        self.assertNotIn('password', res.data)

    def __test_user_info_patch(self, field):
        """función para testear los campos actualizados"""
        payload = {
            field: 'otronombre@mail.com',
        }
        res = self.client.patch(URL_ME, payload)
        user_db = get_user_model().objects.get(
            email=self.user.email
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(getattr(user_db, field), payload[field])

    def test_user_info_fields_patch(self):
        """Testear que la información del usuario se actualiza correctamente"""
        self.__test_user_info_patch('first_name')
        self.__test_user_info_patch('last_name')
        self.__test_user_info_patch('email')

    def test_user_password_change(self):
        """Testear que pide la contraseña de confirmación"""
        res = self.client.patch(
            URL_ME,
            {'password': 'un_solo_password'}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        res = self.client.patch(
            URL_ME,
            {'password_confirmation': 'un_solo_password'}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_change(self):
        """Testear que se cambia la contraseña correctamente"""
        payload = {
            'password': 'new_password',
            'password_confirmation': 'new_password'
        }
        res = self.client.patch(URL_ME, payload)
        is_bad_password = self.user.check_password('password123')
        is_correct_password = self.user.check_password(payload['password'])

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(is_bad_password)
        self.assertTrue(is_correct_password)

    def test_email_is_unique(self):
        """Testear que no se duplique el email al actualizarlo"""
        payload = {
            'email': 'test_user_2@gmail.com',
            'first_name': 'testing1',
            'password': 'password123',
        }
        get_user_model().objects.create_user(**payload)
        res = self.client.patch(URL_ME, {'email': payload['email']})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.user.email, 'test@gmail.com')
