from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from user.models import User
from employee.models import Employee
import json


class APICreateEmployeeTestCase(APITestCase):

    def setUp(self):
        """
        Create a User. Authentication has been disabled
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='123',
        )
        self.client.force_authenticate(self.user)
        self.url = reverse('employee-create')

    def test_create_employee_without_data(self):
        """
        Testing if we can create an employee without any additional field
        """
        payload = json.dumps({})
        response = self.client.post(self.url, payload, content_type='application/json')
        entered_employee = Employee.objects.get(user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(entered_employee.user, self.user)

    def test_create_employee_with_about_yourself_field(self):
        """
        Testing if the employee with the about yourself field has been properly created
        """
        payload = json.dumps({
            'about_yourself': 'test_about_yourself',
        })
        response = self.client.post(self.url, payload, content_type='application/json')
        entered_employee = Employee.objects.get(user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(entered_employee.about_yourself, 'test_about_yourself')

    def test_create_employee_with_city_field(self):
        """
        Testing if the employee with the city field has been properly created
        """
        payload = json.dumps({
            'city': 'test city',
        })
        response = self.client.post(self.url, payload, content_type='application/json')
        entered_employee = Employee.objects.get(user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(entered_employee.city, 'test city')

    def test_create_employee_with_linkdin_field(self):
        """
        Testing if the employee with the linkdin field has been properly created
        """
        payload = json.dumps({
            'linkdin': 'https://www.linkedin.com/in/test/',
        })
        response = self.client.post(self.url, payload, content_type='application/json')
        entered_employee = Employee.objects.get(user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(entered_employee.linkdin, 'https://www.linkedin.com/in/test/')

    def test_create_employee_with_wrong_linkdin_field(self):
        """
        Testing if the employee with a wrong data for the linkdin field has been properly created
        """
        payload = json.dumps({
            'linkdin': 'test',
        })
        response = self.client.post(self.url, payload, content_type='application/json')
        self.assertRaises(Exception, self.client.post(self.url, payload, content_type='application/json'))

    def test_create_employee_with_skills_field(self):
        """
        Testing if the employee with the skills field has been properly created
        """
        payload = json.dumps({
            'skills': [{
                "name": "Python"
            }],
        })
        response = self.client.post(self.url, payload, content_type='application/json')
        entered_employee = Employee.objects.get(user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(entered_employee.skills.all()[0].name, 'Python')

    def test_create_employee_with_status_field(self):
        """
        Testing if the employee with the status field has been properly created
        """
        payload = json.dumps({
            'status': 'Active',
        })
        response = self.client.post(self.url, payload, content_type='application/json')
        entered_employee = Employee.objects.get(user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(entered_employee.status, 'Active')

    def test_create_employee_with_wrong_status_field(self):
        """
        Testing if the employee with a wrong data for the status field has been properly created
        """
        payload = json.dumps({
            'status': 'test',
        })
        response = self.client.post(self.url, payload, content_type='application/json')
        self.assertRaises(Exception, self.client.post(self.url, payload, content_type='application/json'))

    def test_create_employee_with_tags_field(self):
        """
        Testing if the employee with the tags field has been properly created
        """
        payload = json.dumps({
            'tags': 'Engineering',
        })
        response = self.client.post(self.url, payload, content_type='application/json')
        entered_employee = Employee.objects.get(user=self.user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(entered_employee.tags, 'Engineering')

    def test_create_employee_with_wrong_tags_field(self):
        """
        Testing if the employee with a wrong data for the tags field has been properly created
        """
        payload = json.dumps({
            'tags': 'test',
        })
        response = self.client.post(self.url, payload, content_type='application/json')
        self.assertRaises(Exception, self.client.post(self.url, payload, content_type='application/json'))
