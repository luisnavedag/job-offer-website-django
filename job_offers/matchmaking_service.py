from django.db.models.query import QuerySet
from user.models import User
from employee.models import Employee
from job_offers.models import JobOffer
from .models import Matchmaking
from user.email_service.email_service import SendEmail
from abc import ABC, abstractmethod


class PerformMatchmaking(ABC):
    """
    The base class to perform matchmaking
    """

    def __init__(self, data: dict, send_email_obj: SendEmail):
        self.data = data
        self.send_email_obj = send_email_obj

    @abstractmethod
    def perform_matchmaking_for_single_item(self):
        """
        A method that will get a single matchmaking item
        """
        pass

    @abstractmethod
    def send_email(self, *args, **kwargs):
        """
        A method that will send an email notifying you of finding an offer that may interest you
        """
        pass


class PerformMatchmakingJobOfferEmployee(PerformMatchmaking):
    """
    Perform matchmaking for newly added offers. Email users who have active
    matchmaking options and have the required skills from the offer
    """

    def perform_matchmaking_for_single_item(self):
        [self.send_email(employee=employee) for employee in self.get_employees_with_required_skills()]

    def send_email(self, *args, **kwargs):
        employee = kwargs['employee']
        self.data.update({
            'employee': employee,
            'email': User.get_user_email_by_employee_id(employee.id)
        })

        self.send_email_obj.email_data = self.data

        if employee.accept_matchmaking and not self._is_unique_record_already_in_db(employee):
            self.send_email_obj.send_email()

    def get_employees_with_required_skills(self) -> QuerySet:
        """
        Download from the database of users who have skills that may match the offer
        """
        return Employee.objects.filter(skills__in=self._get_job_offer().skills.all()).distinct()

    def _get_job_offer(self) -> JobOffer:
        """
        The function retrieves from the database information about the offer for
        which the matchmaking is carried out
        """
        instance = JobOffer.objects.get(id=self.data['job_offer_id'])
        self.data.update({'job_offer_title': instance.title})

        return instance

    def _is_unique_record_already_in_db(self, employee) -> bool:
        """
        Check if an email with a given offer has already been sent to the user
        """
        if not Matchmaking.objects.filter(employee=employee, job_offer=self._get_job_offer()).exists():
            Matchmaking.objects.create(
                employee=employee,
                job_offer=self._get_job_offer()
            )
            return False
        return True
