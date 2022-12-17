import pytest
from user.models import User


@pytest.fixture
def create_user(db):
    return User.objects.create_user(username="test-user", password="test")


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
