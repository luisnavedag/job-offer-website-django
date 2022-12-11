from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from user.models import User
import json


class APICreateUserTestCase(APITestCase):

    url = reverse('auth_register')

    def test_create_user(self):
        """
        The function checks whether a user will be created for the correct data
        """
        user = {
            "username": "test",
            "first_name": "test",
            "last_name": "test",
            "password": "testing1234",
            "password2": "testing1234",
            "email": "test.grzegorzp@gmail.com"
        }
        payload = json.dumps(user)
        response = self.client.post(self.url, payload, content_type='application/json')

        user = User.objects.get(id=response.data['id'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], user.email)

    def test_create_user_expected_failure(self):
        """
        The function checks whether the user will not be created and
        whether information about missing fields will be returned.
        """
        user = {
            "username": "test",
            "password": "testing1234",
        }
        payload = json.dumps(user)
        response = self.client.post(self.url, payload, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('password2', response.data)
        self.assertIn('email', response.data)


class APIChangePasswordUserTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser',
            password='123',
        )
        self.client.force_authenticate(self.user)

        self.url_change_password = reverse('change_password')

    def test_change_password(self):
        """
        The function checks whether the password change
        for the logged-in user will be carried out correctly
        """
        password = {
            'old_password': '123',
            'new_password': 'test4321',
            'new_password2': 'test4321'
        }

        payload = json.dumps(password)
        response = self.client.put(self.url_change_password, payload, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password('test4321'))

