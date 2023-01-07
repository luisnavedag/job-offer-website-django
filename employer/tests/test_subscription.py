from django.urls import reverse
from rest_framework.test import APIClient
from employer.models import Employer
from employee.models import Employee
import pytest
from datetime import date, timedelta


@pytest.mark.django_db
def test_create_standard_subscription(
        api_client_with_credentials: APIClient,
        create_employer: Employer):
    """
    Test adding a subscription for a standard type
    """
    url = reverse('subscription')
    first_day = get_date(0)
    last_day = get_date(30)
    data = {
        'type': 'Standard',
        'first_day': first_day
    }
    response = api_client_with_credentials.post(url, data=data)
    assert response.status_code == 201

    assert response.data['type'] == 'Standard'
    assert response.data['days'] == 30
    assert response.data['locations'] == 1
    assert response.data['offer_raise'] == 1
    assert response.data['promoting'] is False
    assert response.data['customer_care'] is False
    assert response.data['first_day'] == first_day
    assert response.data['last_day'] == last_day


@pytest.mark.django_db
def test_create_business_subscription(
        api_client_with_credentials: APIClient,
        create_employer: Employer):
    """
    Test adding a subscription for a business type
    """
    url = reverse('subscription')
    first_day = get_date(0)
    last_day = get_date(30)
    data = {
        'type': 'Business',
        'first_day': first_day
    }
    response = api_client_with_credentials.post(url, data=data)
    assert response.status_code == 201

    assert response.data['type'] == 'Business'
    assert response.data['days'] == 30
    assert response.data['locations'] == 2
    assert response.data['offer_raise'] == 2
    assert response.data['promoting'] is True
    assert response.data['customer_care'] is False
    assert response.data['first_day'] == first_day
    assert response.data['last_day'] == last_day


@pytest.mark.django_db
def test_create_pro_subscription(
        api_client_with_credentials: APIClient,
        create_employer: Employer):
    """
    Test adding a subscription for a Pro type
    """
    url = reverse('subscription')
    first_day = get_date(0)
    last_day = get_date(30)
    data = {
        'type': 'Pro',
        'first_day': first_day
    }
    response = api_client_with_credentials.post(url, data=data)
    assert response.status_code == 201

    assert response.data['type'] == 'Pro'
    assert response.data['days'] == 30
    assert response.data['locations'] == 5
    assert response.data['offer_raise'] == 3
    assert response.data['promoting'] is True
    assert response.data['customer_care'] is True
    assert response.data['first_day'] == first_day
    assert response.data['last_day'] == last_day


@pytest.mark.django_db
def test_create_enterprise_subscription(
        api_client_with_credentials: APIClient,
        create_employer: Employer):
    """
    Test adding a subscription for an Enterprise type
    """
    url = reverse('subscription')
    first_day = get_date(0)
    last_day = get_date(30)
    data = {
        'type': 'Enterprise',
        'first_day': first_day
    }
    response = api_client_with_credentials.post(url, data=data)
    assert response.status_code == 201

    assert response.data['type'] == 'Enterprise'
    assert response.data['days'] == 30
    assert response.data['locations'] == 19
    assert response.data['offer_raise'] == 5
    assert response.data['promoting'] is True
    assert response.data['customer_care'] is True
    assert response.data['first_day'] == first_day
    assert response.data['last_day'] == last_day


@pytest.mark.django_db
def test_create_subscription_with_wrong_type(
        api_client_with_credentials: APIClient,
        create_employer: Employer):
    """
    Test whether an error will be returned for the wrong type field
    """
    url = reverse('subscription')
    data = {
        'type': 'test',
        'first_day': get_date(0)
    }
    response = api_client_with_credentials.post(url, data=data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_subscription_with_wrong_data(
        api_client_with_credentials: APIClient,
        create_employer: Employer):
    """
    Test whether an error will be returned for the wrong first_day field
    """
    url = reverse('subscription')
    data = {
        'type': 'Standard',
        'first_day': '2023'
    }
    response = api_client_with_credentials.post(url, data=data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_subscription_for_user_without_permission(
        api_client_with_credentials: APIClient,
        create_employee: Employee):
    """
    Test if an error is returned for a user without permission
    """
    url = reverse('subscription')
    data = {
        'type': 'Standard',
        'first_day': '2023-12-31'
    }
    response = api_client_with_credentials.post(url, data=data)
    assert response.status_code == 403


def test_default_ordering_data(create_subscriptions: APIClient):
    """
    Test the default ordering settings
    """
    url = reverse('subscriptions')
    response = create_subscriptions.get(url)

    assert response.status_code == 200
    assert response.data[0]['last_day'] == get_date(30)
    assert response.data[1]['last_day'] == get_date(32)
    assert response.data[2]['last_day'] == get_date(33)
    assert response.data[3]['last_day'] == get_date(42)
    assert response.data[4]['last_day'] == get_date(53)
    assert response.data[5]['last_day'] == get_date(63)
    assert response.data[6]['last_day'] == get_date(75)
    assert response.data[7]['last_day'] == get_date(90)


def test_ordering_by_created_field(create_subscriptions: APIClient):
    """
    Test ordering for field created
    """
    url = reverse('subscriptions') + '?ordering=created'
    response = create_subscriptions.get(url)

    assert response.status_code == 200
    assert response.data[0]['id'] == 1
    assert response.data[1]['id'] == 2
    assert response.data[2]['id'] == 3
    assert response.data[3]['id'] == 4
    assert response.data[4]['id'] == 5
    assert response.data[5]['id'] == 6
    assert response.data[6]['id'] == 7
    assert response.data[7]['id'] == 8


def test_ordering_by_type_field(create_subscriptions: APIClient):
    """
    Test ordering for field type
    """
    url = reverse('subscriptions') + '?ordering=type'
    response = create_subscriptions.get(url)

    assert response.status_code == 200
    assert response.data[0]['type'] == 'Business'
    assert response.data[1]['type'] == 'Business'
    assert response.data[2]['type'] == 'Enterprise'
    assert response.data[3]['type'] == 'Pro'
    assert response.data[4]['type'] == 'Pro'
    assert response.data[5]['type'] == 'Standard'
    assert response.data[6]['type'] == 'Standard'
    assert response.data[7]['type'] == 'Standard'


def test_filtering_by_type_field_as_business(create_subscriptions: APIClient):
    """
    Test filtering for field Business
    """
    url = reverse('subscriptions') + '?type=Business'
    response = create_subscriptions.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['type'] == 'Business'
    assert response.data[1]['type'] == 'Business'


def test_filtering_by_type_field_as_standard(create_subscriptions: APIClient):
    """
    Test filtering for field Standard
    """
    url = reverse('subscriptions') + '?type=Standard'
    response = create_subscriptions.get(url)

    assert response.status_code == 200
    assert len(response.data) == 3
    assert response.data[0]['type'] == 'Standard'
    assert response.data[1]['type'] == 'Standard'
    assert response.data[2]['type'] == 'Standard'


@pytest.fixture
@pytest.mark.django_db
def create_subscriptions(api_client_with_credentials: APIClient, create_employer: Employer):
    """
    Create different subscriptions for testing purposes
    """
    url = reverse('subscription')
    data = [
        {'type': 'Standard', 'first_day': get_date(60)},
        {'type': 'Pro', 'first_day': get_date(23)},
        {'type': 'Business', 'first_day': get_date(33)},
        {'type': 'Standard', 'first_day': get_date(0)},
        {'type': 'Business', 'first_day': get_date(3)},
        {'type': 'Pro', 'first_day': get_date(2)},
        {'type': 'Enterprise', 'first_day': get_date(12)},
        {'type': 'Standard', 'first_day': get_date(45)}
    ]
    [api_client_with_credentials.post(url, data=data[x]) for x, _ in enumerate(data)]
    return api_client_with_credentials


def get_date(value: int) -> str:
    """
    The function returns the date in text format
    """
    date_ = date.today() + timedelta(days=value)
    return date_.strftime("%Y-%m-%d")
