from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from employee.models import Skill
import json


class APICreateSkillTestCase(APITestCase):

    def setUp(self):
        """
        Create a User. Authentication has been disabled
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='123',
        )
        self.client.force_authenticate(self.user)
        self.url = reverse('skill-create')

    def test_create_skill(self):
        """
        Test creating data for authenticated user
        """
        skill = "Django"

        payload = json.dumps({
            "name": skill
        })

        response = self.client.post(self.url, payload, content_type='application/json')
        entered_skill = Skill.objects.get(name=skill)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(entered_skill.name, skill)

