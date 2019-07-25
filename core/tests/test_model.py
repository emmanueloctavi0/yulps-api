from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def test_create_user_with_email(self):
        """Test para crear un usuario con su email"""
        payload = {
            'email': 'email_test@gmail.com',
            'password': 'password123',
        }
        user = get_user_model().objects.create_user(**payload)
        self.assertEqual(payload['email'], user.email)
        self.assertTrue(user.check_password(payload['password']))

    def test_raise_message_with_blank_email(self):
        """Se lanza una excepción con un email en blanco"""
        payload = {
            'email': '',
            'password': 'password123',
        }

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(**payload)
