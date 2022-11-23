from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from employee.models import Employee, Skill
import json


class APIDetailEmployeeTestCase(APITestCase):

    def setUp(self):
        """
        Create a User. Authentication has been disabled
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='123',
        )
        self.client.force_authenticate(self.user)
        self.url = reverse('employee-detail', kwargs={'pk': 1})

    def test_get_employee_for_authenticated_user(self):
        """
        Test getting data for authenticated user
        """
        Employee.objects.create(user=self.user)

        response = self.client.get(self.url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)

    def test_get_employee_for_authenticated_user_with_skills_field(self):
        """
        Test getting data for authenticated user with skills filed
        """
        skill_1 = Skill.objects.create(name="Django")
        skill_2 = Skill.objects.create(name="Flask")

        employee = Employee.objects.create(user=self.user)
        employee.skills.add(skill_1, skill_2)

        response = self.client.get(self.url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['skills'][0]['name'], "Django")
        self.assertEqual(response.data['skills'][1]['name'], "Flask")

    def test_update_employee_for_authenticated_user(self):
        """
        Test updating data for authenticated user
        """
        Employee.objects.create(user=self.user)

        payload = json.dumps({
            'city': 'test city',
        })
        response = self.client.put(self.url, payload, content_type='application/json')

        entered_employee = Employee.objects.get(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(entered_employee.city, "test city")

    def test_update_employee_for_authenticated_user_with_skills_field(self):
        """
        Test updating data for authenticated user with skills field
        """
        Employee.objects.create(user=self.user)

        payload = json.dumps({
            'skills': [{
                "name": "Python"
            }],
        })
        response = self.client.put(self.url, payload, content_type='application/json')

        entered_employee = Employee.objects.get(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(entered_employee.skills.all()[0].name, 'Python')

    def test_delete_employee(self):
        """
        Test deleting employee
        """
        Employee.objects.create(user=self.user)

        response = self.client.delete(self.url, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Employee.objects.all()), 0)
