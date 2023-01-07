from django.urls import reverse
from rest_framework.test import APIClient
from job_offers.tests.data_for_tests import create_data


def test_job_offers_with_available_date(api_client_with_credentials: APIClient, create_data: list):
    """
    The function checks whether job offers that are not in the appropriate range will not be returned
    """
    url = reverse('job-offers')

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 10


def test_correctness_of_boosting_for_job_offers(api_client_with_credentials: APIClient, create_data: list):
    """
    The function checks whether the offers have been properly raised
    and whether they are arranged in ascending order
    """
    url = reverse('job-offers')

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert [x['days_to_raise'] for x in response.data] == [0, 0, 0, 1, 2, 3, 4, 4, 6, 7]


def test_filtering_job_offers_by_tags_engineering(api_client_with_credentials: APIClient, create_data: list):
    """
    The function returns only available offers with the Engineering tag
    """
    url = reverse('job-offers') + '?tags=Engineering'

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3
    assert all(True if x['tags'] == 'Engineering' else False for x in response.data)


def test_filtering_job_offers_by_tags_design(api_client_with_credentials: APIClient, create_data: list):
    """
    The function returns only available offers with the Design tag
    """
    url = reverse('job-offers') + '?tags=Design'

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
    assert all(True if x['tags'] == 'Design' else False for x in response.data)


def test_filtering_job_offers_by_min_amount(api_client_with_credentials: APIClient, create_data: list):
    """
    The function returns only available offers with salary from 2500
    """
    url = reverse('job-offers') + '?min_amount=2500'

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
    assert all(True if float(x['salary_from']) >= 2500 else False for x in response.data)


def test_filtering_job_offers_by_max_amount(api_client_with_credentials: APIClient, create_data: list):
    """
    The function returns only available offers with salary up to 1500
    """
    url = reverse('job-offers') + '?max_amount=1500'

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3
    assert all(True if float(x['salary_up_to']) <= 1500 else False for x in response.data)


def test_filtering_job_offers_by_min_and_max_amount(api_client_with_credentials: APIClient, create_data: list):
    """
    The function returns only available offers with salary between 1000 and 2500
    """
    url = reverse('job-offers') + '?min_amount=1000&max_amount=2500'

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3
    assert all(True if (float(x['salary_from']) >= 1000 and float(x['salary_up_to']) <= 2500) else False for x in response.data)


def test_filtering_job_offers_by_experience_intership(api_client_with_credentials: APIClient, create_data: list):
    """
    The function returns only available offers with the Internship/Junior experience
    """
    url = reverse('job-offers') + '?experience=Internship/Junior'

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3
    assert all(True if x['experience'] == 'Internship/Junior' else False for x in response.data)


def test_filtering_job_offers_by_experience_senior(api_client_with_credentials: APIClient, create_data: list):
    """
    The function returns only available offers with the Senior experience
    """
    url = reverse('job-offers') + '?experience=Senior'

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3
    assert all(True if x['experience'] == 'Senior' else False for x in response.data)


def test_filtering_job_offers_by_form_of_employment_full_time(api_client_with_credentials: APIClient, create_data: list):
    """
    The function returns only available offers with the Full-time form of employment
    """
    url = reverse('job-offers') + '?form_of_employment=Full-time'

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 4
    assert all(True if x['form_of_employment'] == 'Full-time' else False for x in response.data)


def test_filtering_job_offers_by_form_of_employment_part_time(api_client_with_credentials: APIClient, create_data: list):
    """
    The function returns only available offers with the Part time form of employment
    """
    url = reverse('job-offers') + '?form_of_employment=Part-time'

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert all(True if x['form_of_employment'] == 'Part-time' else False for x in response.data)


def test_filtering_job_offers_by_operationg_mode_remote_work(api_client_with_credentials: APIClient, create_data: list):
    """
    The function returns only available offers with the Remote work operating mode
    """
    url = reverse('job-offers') + '?operationg_mode=Remote-work'

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5
    assert all(True if x['operationg_mode'] == 'Remote-work' else False for x in response.data)


def test_filtering_job_offers_by_operationg_mode_on_site(api_client_with_credentials: APIClient, create_data: list):
    """
    The function returns only available offers with the On-site operating mode
    """
    url = reverse('job-offers') + '?operationg_mode=On-site'

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2
    assert all(True if x['operationg_mode'] == 'On-site' else False for x in response.data)


def test_filtering_job_offers_by_city_cracow(api_client_with_credentials: APIClient, create_data: list):
    """
    The function returns only available offers with Cracow city
    """
    url = reverse('job-offers') + '?location=Cracow'

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 7


def test_filtering_job_offers_by_city_warszawa(api_client_with_credentials: APIClient, create_data: list):
    """
    The function returns only available offers with Warszawa city
    """
    url = reverse('job-offers') + '?location=Warszawa'

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2


def test_filtering_job_offers_by_working_time_full_time(api_client_with_credentials: APIClient, create_data: list):
    """
    The function returns only available offers with working time Full-time
    """
    url = reverse('job-offers') + '?working_time=Full-time'

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 7
    assert all(True if x['working_time'] == 'Full-time' else False for x in response.data)


def test_filtering_job_offers_by_working_time_internship(api_client_with_credentials: APIClient, create_data: list):
    """
    The function returns only available offers with working time Full-time
    """
    url = reverse('job-offers') + '?working_time=Internship'

    response = api_client_with_credentials.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert all(True if x['working_time'] == 'Internship' else False for x in response.data)
