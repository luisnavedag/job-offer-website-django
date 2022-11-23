from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from employee.models import Skill, Employee


class APIFilterSearchEmployeesTestCase(APITestCase):

    def setUp(self):
        """
        Create a User. Authentication has been disabled
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='123',
        )
        self.client.force_authenticate(self.user)

    def test_get_all_data(self):
        """
        Test if all data will be returned
        """
        self.create_data()

        url = "/api/employees/"

        response = self.client.get(url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filtering_tags(self):
        """
        Test filtering tags for word Marketing
        """
        self.create_data()

        url = "/api/employees/?tags=Marketing"

        response = self.client.get(url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['tags'], "Marketing")
        self.assertEqual(len(response.data), 1)

    def test_filtering_status(self):
        """
        Test filtering status for word Active
        """
        self.create_data()

        url = "/api/employees/?status=Active"

        response = self.client.get(url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['status'], "Active")
        self.assertEqual(len(response.data), 1)

    def test_filtering_skills(self):
        """
        Test filtering skills for word Python
        """
        self.create_data()

        url = "/api/employees/?skills__name=Python"

        response = self.client.get(url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['skills'][0]['name'], "Python")
        self.assertEqual(len(response.data), 1)

    def test_searching_city(self):
        """
        Test searching city for word London
        """
        self.create_data()

        url = "/api/employees/?search=London"

        response = self.client.get(url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['city'], "London")
        self.assertEqual(len(response.data), 1)

    @staticmethod
    def create_data():
        """
        Create data for testing
        """
        instance_1 = Employee.objects.create(
            tags="Marketing",
            city="London",
            linkdin="www.test.com",
            status="Active",
            about_yourself="test"
        )
        s1 = Skill.objects.create(name="Python")
        s1.save()
        instance_1.skills.add(s1)

        instance_2 = Employee.objects.create(
            tags="Sales",
            city="Amsterdam",
            linkdin="www.test1.com",
            status="Open",
            about_yourself="test"
        )
        s2 = Skill.objects.create(name="Django")
        s2.save()
        instance_2.skills.add(s2)
