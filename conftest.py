import pytest
from user.models import User
from employer.models import Employer, Subscription, Payment
from employee.models import Employee
from rest_framework.test import APIClient
from job_offers.models import JobOffer
from datetime import date, timedelta
from employer.static import *


@pytest.fixture
def create_user(db) -> User:
    """
    The function creates a new user for the sample data
    """
    return User.objects.create_user(
        username="test-user",
        password="test"
    )


@pytest.fixture
def create_employer(db, create_user: User) -> Employer:
    """
    The function creates a new employer for the sample data
    """
    return Employer.objects.create(
        user=create_user,
        company_name='test',
        company_size=1,
        website='https://test.pl/',
    )


@pytest.fixture
def create_employee(db, create_user: User) -> Employee:
    """
    The function creates a new employee for the sample data
    """
    return Employee.objects.create(
        user=create_user,
        tags="Engineering",
        city="Test",
        status="Active"
    )


@pytest.fixture
def create_payment(db) -> Payment:
    """
    The function creates a new payment for the sample data
    """
    return Payment.objects.create()


@pytest.fixture
def create_job_offer(db) -> JobOffer:
    """
    The function creates a new job offer for sample data.
    """
    return JobOffer.objects.create()


@pytest.fixture
def create_standard_subscription(
        db,
        create_employer: Employer,
        create_payment: Payment,
        create_job_offer: JobOffer) -> Subscription:
    """
    The function creates a new subscription for sample data.
    The employer, payment, and job offer will be passed in the relationship via fixture
    """
    return Subscription.objects.create(
        employer=create_employer,
        payment=create_payment,
        job_offer=create_job_offer,
        type='Standard',
        days=Standard.DAYS.value,
        locations=Standard.LOCATIONS.value,
        offer_raise=Standard.OFFER_RAISE.value,
        promoting=Standard.PROMOTING.value,
        customer_care=Standard.CUSTOMER_CARE.value,
        created=date.today(),
        first_day=date.today(),
        last_day=date.today() + timedelta(days=30)
    )


@pytest.fixture
def api_client() -> APIClient:
    """
    The function returns APIClient object
    """
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, create_user: User, api_client: APIClient) -> APIClient:
    """
    The function returns an APIClient object. The user has been authenticated.
    By using yield the credentials will be cleared after each test
    """
    user = create_user
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
