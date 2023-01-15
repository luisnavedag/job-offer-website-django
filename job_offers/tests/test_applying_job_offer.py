from django.urls import reverse
from rest_framework.test import APIClient
from employee.models import Employee
from employer.models import Employer
from job_offers.models import JobOffer
from job_offers.tests.data_for_tests import create_data


def test_applying_for_job_by_employee(
        api_client_with_credentials: APIClient,
        create_data: list,
        create_employee: Employee):
    """
    Test whether the employee can apply for the position
    """
    job_offer_id = JobOffer.objects.all()[0].id
    url = reverse('job-offer-application', args=[job_offer_id])

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200


def test_applying_for_job_by_employer(
        api_client_with_credentials: APIClient,
        create_data: list,
        create_employer: Employer):
    """
    Test whether the employer can apply for the position
    """
    url = reverse('job-offer-application', args=[1])

    response = api_client_with_credentials.get(url)
    assert response.status_code == 403


def test_applying_for_job_by_unauthenticated_user(api_client_with_credentials: APIClient, create_data: list):
    """
    Test whether a person who is not logged in can apply for the position
    """
    url = reverse('job-offer-application', args=[1])

    response = api_client_with_credentials.get(url)
    assert response.status_code == 403


def test_applying_for_the_same_job_by_employee_twice(
        api_client_with_credentials: APIClient,
        create_data: list,
        create_employee: Employee):
    """
    Test whether a user can apply twice for the same position
    """
    job_offer_id = JobOffer.objects.all()[0].id
    url = reverse('job-offer-application', args=[job_offer_id])

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    response = api_client_with_credentials.get(url)
    assert response.status_code == 400
