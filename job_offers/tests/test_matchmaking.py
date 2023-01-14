import pytest
from rest_framework.test import APIClient
from datetime import datetime, timedelta
from job_offers.matchmaking_service import PerformMatchmakingJobOfferEmployee
from job_offers.email_service import SendEmailJobOfferMatchmaking
from .data_for_tests import create_employees, create_data


def get_time_stamp_5_min() -> float:
    """
    The function returns the current timestamp with 5 minutes added
    """
    dt = datetime.now() + timedelta(minutes=5)
    return datetime.timestamp(dt)


def test_matchmaking_for_skills_python_pytest(
        api_client_with_credentials: APIClient, create_data: list, create_employees: list):
    """
    Test if users are properly matched for python or pytest skills
    """
    data = {
        'job_offer_id': 1,
    }
    instance = PerformMatchmakingJobOfferEmployee(data, SendEmailJobOfferMatchmaking())
    employees = instance.get_employees_with_required_skills()

    assert len(employees) == 2

    for employee in employees:
        assert any([True for skill in employee.skills.all() if skill.name == "Python" or skill.name == "Pytest"])


def test_matchmaking_for_skills_google_ads_google_analytics(
        api_client_with_credentials: APIClient, create_data: list, create_employees: list):
    """
    Test if users are properly matched for Google Ads or Google Analytics
    """

    data = {
        'job_offer_id': 2,
    }
    instance = PerformMatchmakingJobOfferEmployee(data, SendEmailJobOfferMatchmaking())
    employees = instance.get_employees_with_required_skills()

    assert len(employees) == 1

    for employee in employees:
        assert any([True for skill in employee.skills.all()
                    if skill.name == "Google Ads" or skill.name == "Google Analytics"])


def test_matchmaking_for_skill_ms_office(
        api_client_with_credentials: APIClient, create_data: list, create_employees: list):
    """
    Test if users are properly matched for MS Office
    """

    data = {
        'job_offer_id': 4,
    }
    instance = PerformMatchmakingJobOfferEmployee(data, SendEmailJobOfferMatchmaking())
    employees = instance.get_employees_with_required_skills()

    assert len(employees) == 2

    for employee in employees:
        assert any([True for skill in employee.skills.all() if skill.name == "MS Office"])


def test_matchmaking_for_skill_java_and_sql(
        api_client_with_credentials: APIClient, create_data: list, create_employees: list):
    """
    Test if users are properly matched for Java or SQL or Spring
    """

    data = {
        'job_offer_id': 7,
    }
    instance = PerformMatchmakingJobOfferEmployee(data, SendEmailJobOfferMatchmaking())
    employees = instance.get_employees_with_required_skills()

    assert len(employees) == 3

    for employee in employees:
        assert any([True for skill in employee.skills.all()
                    if skill.name == "Java" or skill.name == "SQL" or skill.name == "Spring"])
