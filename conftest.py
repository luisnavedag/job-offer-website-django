import pytest
from user.models import User
from employer.models import Employer
from employee.models import Employee


@pytest.fixture
def create_user(db):
    return User.objects.create_user(
        username="test-user",
        password="test"
    )


@pytest.fixture
def create_employer(db, create_user):
    return Employer.objects.create(
        user=create_user,
        company_name='test',
        company_size=1,
        website='https://test.pl/',
    )


@pytest.fixture
def create_employee(db, create_user):
    return Employee.objects.create(
        user=create_user,
        tags="Engineering",
        city="Test",
        status="Active"
    )


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, create_user, api_client):
    user = create_user
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
