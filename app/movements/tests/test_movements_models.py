from django.test import TestCase
from django.contrib.auth import get_user_model

from movements.models import MovementCategory, Movement


class TestMovementCategoryModel(TestCase):
    """Test model Category"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            first_name='nombre test',
            password='password123'
        )

    def test_create_new_category_movement(self):
        """Verificar que se crea correctamente una categoria de movimiento"""
        category = MovementCategory(
            name='Comida',
            description='Comida diaria',
            user=self.user
        )
        category.save()
        category_db = MovementCategory.objects.get(name='Comida')
        self.assertEqual(category.name, category_db.name)


class TestMovementModel(TestCase):
    """Test model Movement"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            first_name='nombre test',
            password='password123'
        )
        self.category = MovementCategory(
            name='Comida',
            description='Comida diaria',
            user=self.user
        )
        self.category.save()

    def test_create_new_movement(self):
        """Testear el modelo movement"""
        movement = Movement.objects.create(
            detail='Comida en la sartén',
            mount=70,
            user=self.user,
            category=self.category
        )
        movement_db = Movement.objects.get(
            detail='Comida en la sartén'
        )
        self.assertEqual(movement.detail, movement_db.detail)
        self.assertEqual(movement.user, movement_db.user)
        self.assertEqual(movement.category, movement_db.category)
