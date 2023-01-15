from rest_framework.test import APITestCase
from rest_framework import status
from user.models import User
from employee.models import Skill


class APIFilterSearchSkillsTestCase(APITestCase):

    def setUp(self):
        """
        Create a User. Authentication has been disabled
        """
        self.user = User.objects.create_superuser(
            username='testuser',
            password='123',
        )
        # self.user.is_active = True
        self.client.force_authenticate(self.user)

    def test_get_all_data(self):
        """
        Test if all data will be returned
        """
        self.create_data()

        url = "/api/skills/"

        response = self.client.get(url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_filtering_name(self):
        """
        Test filtering name for word Python
        """
        self.create_data()

        url = "/api/skills/?name=Python"

        response = self.client.get(url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], "Python")
        self.assertEqual(len(response.data), 1)

    def test_searching_python(self):
        """
        Test searching name for word Python
        """
        self.create_data()

        url = "/api/skills/?search=Python"

        response = self.client.get(url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @staticmethod
    def create_data():
        """
        Create data for testing
        """
        Skill.objects.create(name="Python")
        Skill.objects.create(name="Django")
        Skill.objects.create(name="Flask")
        Skill.objects.create(name="Python3.11")

