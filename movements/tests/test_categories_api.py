from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from movements.models import MovementCategory


URL_CATEGORY = reverse('movement:categories-list')


def url_category_detail(category_id):
    """Crear la url con un id"""
    return reverse('movement:categories-detail', args=[category_id])


def create_new_user(email, password='password123', first_name='name_test'):
    """Crear un usario de prueba"""
    return get_user_model().objects.create_user(
        email=email,
        password=password,
        first_name=first_name
    )


def create_category(user, name, description='desc'):
    """Crear una categoria"""
    return MovementCategory.objects.create(
        user=user,
        name=name,
        description=description
    )


class TestCategoryPublicApi(TestCase):
    """Testear endpoint de categorias sin authenticar"""
    def setUp(self):
        self.client = APIClient()

    def test_authentication_is_required(self):
        """Testear que la autenticación es obligatoria"""
        res = self.client.get(URL_CATEGORY)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('id', res.data)
        self.assertNotIn('name', res.data)


class TestCategoryPrivateApi(TestCase):
    """Testear los endpoints de categoria"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_new_user('test@gmail.com')
        self.client.force_authenticate(user=self.user)

    def test_category_list_is_retrieved(self):
        """Verificar que las categorias se muestran correctamente"""
        cat_1 = create_category(user=self.user, name='Cat1')
        cat_2 = create_category(user=self.user, name='Cat2')

        other_user = create_new_user('test2@gmail.com')
        create_category(user=other_user, name='Cat3')

        res = self.client.get(URL_CATEGORY)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['name'], cat_1.name)
        self.assertEqual(res.data[1]['name'], cat_2.name)

    def test_category_detail_is_retrieved(self):
        """Testear el endpoint con un ID"""
        cat_1 = create_category(user=self.user, name='Cat1')
        cat_2 = create_category(user=self.user, name='Cat2')

        other_user = create_new_user('test2@gmail.com')
        cat_3 = create_category(user=other_user, name='Cat3')

        res = self.client.get(url_category_detail(cat_3.id))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        res = self.client.get(url_category_detail(cat_2.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], cat_2.name)

        res = self.client.get(url_category_detail(cat_1.id))
        self.assertEqual(res.data['name'], cat_1.name)

    def test_category_is_created_successfuly(self):
        """Testear que se crea una categoria correctamente"""
        payload = {
            'name': 'cate_1 test',
            'description': 'categoria de test 1',
        }
        res = self.client.post(URL_CATEGORY, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        category_db = MovementCategory.objects.get(user=self.user)
        self.assertEqual(category_db.name, payload['name'])
        self.assertEqual(category_db.description, payload['description'])
        self.assertEqual(category_db.user, self.user)
