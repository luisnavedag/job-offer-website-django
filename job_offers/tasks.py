from celery import shared_task
from .matchmaking_service import PerformMatchmakingJobOfferEmployee
from .email_service import SendEmailJobOfferMatchmaking


@shared_task
def send_matchmaking_email(data: dict) -> bool:
    """
    A shared function that passes the execution of a task to Celery
    """
    PerformMatchmakingJobOfferEmployee(data, SendEmailJobOfferMatchmaking()).perform_matchmaking_for_single_item()
    return True
