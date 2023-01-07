import pytest
from django.urls import reverse
from job_offers.models import JobOffer
from rest_framework.test import APIClient
from user.models import User
from employer.models import Subscription


@pytest.mark.django_db
def test_updating_job_offer_without_required_fields(
        api_client_with_credentials: APIClient,
        create_standard_subscription: Subscription):
    """
    Testing updating job offer in case we don't provide all required fields
    """
    pk = create_standard_subscription.job_offer.id
    url = reverse('job-offer-detail', args=[pk])

    data = {
        'title': 'Python programmer',
    }
    response = api_client_with_credentials.put(url, data=data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_updating_job_offer(
        api_client_with_credentials: APIClient,
        create_standard_subscription: Subscription,
        job_offer_data: dict[str, any]):
    """
    Testing updating job offer in case we provide all required fields
    """
    pk = create_standard_subscription.job_offer.id
    url = reverse('job-offer-detail', args=[pk])

    response = api_client_with_credentials.put(url, data=job_offer_data, format='json')
    print(response.data)
    assert response.status_code == 200
    assert response.data['title'] == job_offer_data['title']
    assert response.data['cities'][0]['name'] == job_offer_data['cities'][0]['name']
    assert response.data['skills'][0]['name'] == job_offer_data['skills'][0]['name']
    assert response.data['skills_nice_to_have'][0]['name'] == job_offer_data['skills_nice_to_have'][0]['name']
    assert response.data['job_description'] == job_offer_data['job_description']
    assert response.data['address'] == job_offer_data['address']
    assert response.data['information_clause'] == job_offer_data['information_clause']
    assert response.data['contact_name'] == job_offer_data['contact_name']
    assert response.data['contact_email'] == job_offer_data['contact_email']
    assert response.data['contact_phone'] == job_offer_data['contact_phone']


@pytest.mark.django_db
def test_updating_job_offer_with_verified_field(
        api_client_with_credentials: APIClient,
        create_standard_subscription: Subscription,
        job_offer_data: dict[str, any]):
    """
    Testing that a normal user has no way to verify the offer
    """
    pk = create_standard_subscription.job_offer.id
    url = reverse('job-offer-detail', args=[pk])

    job_offer_data.update({'verified': 'True'})

    response = api_client_with_credentials.put(url, data=job_offer_data, format='json')
    assert response.status_code == 200
    assert JobOffer.objects.get(id=create_standard_subscription.job_offer.id).verified is False


@pytest.mark.django_db
def test_updating_job_offer_by_different_user_than_author(
        create_standard_subscription: Subscription,
        job_offer_data: dict[str, any]):
    """
    Testing if a user who is not the author of a job offer can update the offer
    """
    user = User.objects.create_user(
        username="test-user2",
        password="test"
    )
    api_client = APIClient()
    api_client.force_authenticate(user=user)

    pk = create_standard_subscription.job_offer.id
    url = reverse('job-offer-detail', args=[pk])

    response = api_client.put(url, data=job_offer_data, format='json')
    assert response.status_code == 403


@pytest.fixture
def job_offer_data() -> dict[str, any]:
    """
    Sample data to check the correct operation of the API for Job Offer
    """
    return {
        'title': 'Python programmer',
        'cities': [{'name': 'Cracow'}],
        'skills': [{'name': 'Python'}],
        'skills_nice_to_have': [{'name': 'SQL'}],
        'tags': 'Engineering',
        'experience': 'Internship/Junior',
        'form_of_employment': 'Full-time',
        'job_description': 'Lorem Ipsum is simply dummy text of the printing',
        'address': 'Cracow, Rynek',
        'operationg_mode': 'On-site',
        'working_time': 'Full-time',
        'information_clause': 'Lorem Ipsum is simply dummy text of the printing',
        'contact_name': 'John Doe',
        'contact_email': 'johndoe@op.pl',
        'contact_phone': '+48502502502',
    }