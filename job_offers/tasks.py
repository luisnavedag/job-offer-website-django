from .matchmaking_service import PerformMatchmakingJobOfferEmployee
from job_offers.email_service.email_service import SendEmailJobOfferMatchmaking
from job_offers.email_service.job_offer_matchmaking_form import job_offer_matchmaking_email_form
from celery import shared_task


@shared_task
def send_matchmaking_email(data: dict) -> bool:
    """
    A shared function that passes the execution of a task to Celery
    """
    PerformMatchmakingJobOfferEmployee(
        data,
        SendEmailJobOfferMatchmaking(job_offer_matchmaking_email_form)).perform_matchmaking_for_single_item()
    return True
