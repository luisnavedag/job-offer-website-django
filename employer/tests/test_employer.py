import pytest
from django.urls import reverse
from ..models import Employer
from user.models import User


@pytest.mark.django_db
def test_create_employer(api_client_with_credentials, create_user):
    """
    Testing if we can create an employer without any additional field
    """
    url = reverse('employer-list')
    data = {
        'user': create_user.username,
    }
    response = api_client_with_credentials.post(url, data=data)
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_employer(api_client_with_credentials, create_user):
    """
    Testing if we can create an employer
    """
    url = reverse('employer-list')
    data = {
        'user': create_user.username,
        'company_name': 'test',
        'company_size': 1,
        'website': 'https://test.pl/',
    }
    response = api_client_with_credentials.post(url, data=data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_retrieve_employer(api_client_with_credentials, create_user):
    """
    Test getting data for authenticated user
    """
    Employer.objects.create(
        user=create_user,
        company_name='test',
        company_size=1,
        website='https://test.pl/',
    )

    url = reverse('employer-list')

    response = api_client_with_credentials.get(url + '1/')
    assert response.status_code == 200
    assert response.data['website'] == 'https://test.pl/'


@pytest.mark.django_db
def test_update_employer(api_client_with_credentials, create_user):
    """
    Test updating data for authenticated user
    """
    Employer.objects.create(
        user=create_user,
        company_name='test',
        company_size=1,
        website='https://test.pl/',
    )
    data = {
        'company_name': 'test',
        'company_size': 1,
        'website': 'https://new-test.pl/',
    }

    url = reverse('employer-list')

    response = api_client_with_credentials.put(url + '1/', data=data)
    assert response.status_code == 200
    assert Employer.objects.get(user=create_user).website == 'https://new-test.pl/'


@pytest.mark.django_db
def test_remove_employer(api_client_with_credentials, create_user):
    """
    Testing the removal of the employer and the user that will be removed automatically via signals
    """
    Employer.objects.create(
        user=create_user,
        company_name='test',
        company_size=1,
        website='https://test.pl/',
    )

    url = reverse('employer-list')

    response = api_client_with_credentials.delete(url + '1/')
    assert response.status_code == 204
    assert Employer.objects.all().exists() is False
    assert User.objects.all().exists() is False
