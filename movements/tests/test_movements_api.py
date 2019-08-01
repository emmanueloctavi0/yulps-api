from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from movements import models


URL_MOVEMENT = reverse('movement:movements-list')


def create_new_user(email, password='password123', first_name='test name'):
    """Crear un nuevo usuario"""
    return get_user_model().objects.create_user(
        email=email,
        password=password,
        first_name=first_name
    )


class TestMovementPublicApi(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_is_user_authenticated(self):
        """El usuario tiene que estar autenticado"""
        res = self.client.get(URL_MOVEMENT)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestMovementPrivateApi(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = create_new_user(email='test@gmail.com')
        self.client.force_authenticate(user=self.user)

        self.category = models.MovementCategory.objects.create(
            name='Comida',
            description='Comida diaria',
            user=self.user
        )

    def test_create_new_movement(self):
        """Se crea correctamente un movimiento"""
        payload = {
            'detail': 'Sartén Fonda',
            'mount': 70,
            'category': self.category.id,
        }
        res = self.client.post(URL_MOVEMENT, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Verificar que esté en la BD
        movement = models.Movement.objects.get(
            user=self.user
        )

        self.assertEqual(res.data['id'], movement.id)
        self.assertEqual(payload['detail'], movement.detail)
        self.assertEqual(payload['mount'], movement.mount)
        self.assertEqual(payload['category'], movement.category.id)
        self.assertEqual(self.user, movement.user)

    def __field_is_required(self, payload):
        """Funcion para testear un mal payload"""
        res = self.client.post(URL_MOVEMENT, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Verificar que no se guardó en la BD
        movement = models.Movement.objects.filter(
            user=self.user
        )

        self.assertEqual(len(movement), 0)

    def test_fields_are_required(self):
        """Tester multiples payloads"""
        payload = {
            'mount': 70,
            'category': self.category.id,
        }
        self.__field_is_required(payload)

        payload['detail'] = ''
        self.__field_is_required(payload)

        payload['detail'] = 'testing'
        payload['mount'] = ''
        self.__field_is_required(payload)

        payload.pop('mount')
        self.__field_is_required(payload)

        payload['mount'] = 120
        payload['category'] = ''
        self.__field_is_required(payload)

        payload.pop('category')
        self.__field_is_required(payload)

    def test_user_cant_use_other_user_category(self):
        """
        Un usuario no puede asignar a un movimiento
        de una categoria que no le pertenece
        """
        other_user = create_new_user(email='test_332@gmail.com')
        category = models.MovementCategory.objects.create(
            name='Comida',
            description='Comida diaria',
            user=other_user
        )

        payload = {
            'detail': 'Sartén Fonda',
            'mount': 70,
            'category': category.id
        }
        self.__field_is_required(payload)
