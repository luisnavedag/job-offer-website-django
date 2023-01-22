from django.core.mail import EmailMultiAlternatives
from rest_framework.reverse import reverse
from general_utils.email_service.email_service import SendEmail
from user.models import User
from general_utils.url_service import get_full_url
from decouple import config
from pathlib import Path
import datetime


class SendEmailJobOfferVerification(SendEmail):
    """
    The class is used to send an e-mail to the admin to check the correctness of the entered data
    """

    def send_email(self):
        self.get_body()
        email = super().send_email()
        email.send()

    def _get_obj(self) -> EmailMultiAlternatives:
        email = EmailMultiAlternatives(
            subject=f'Verification of the job offer - {self.data["title"]}',
            to=[config('JOB_VERIFICATION_ADMIN_EMAIL')]
        )
        email.content_subtype = 'html'
        email.attach_alternative(self.body, "text/html")
        email.mixed_subtype = 'related'
        email.attach(self._add_header_with_file(self.paths[0]))
        return email

    def get_body(self) -> None:
        self.data.update({
            "url": self._get_verification_link(),
            "image_name": Path(self.paths[0]).name
        })
        self.body = self.html_form(self.data)

    @staticmethod
    def _get_timestamp() -> datetime:
        return datetime.datetime.utcnow().timestamp() + 86400000

    @get_full_url
    def _get_verification_link(self) -> str:
        """
        The function returns the URL that will be verified by the added job offer
        """
        url = reverse('job_offer_verification', kwargs={'pk': self.data['id']})
        return rf"{url}?title={self.data['title']}&expiration_timestamp={self._get_timestamp()}"


class SendEmailJobOfferNewApplication(SendEmail):
    """
    Email a user about an approval of his application for a given position
    """

    def send_email(self):
        self.get_body()
        email = super().send_email()
        email.content_subtype = 'html'
        email.send()

    def _get_obj(self) -> EmailMultiAlternatives:
        email = EmailMultiAlternatives(
            subject=f'The application for your job offer - {self.data["job_offer_title"]}, has just been submitted!',
            to=[self.data['email']])
        email.content_subtype = 'html'
        email.attach_alternative(self.body, "text/html")
        email.mixed_subtype = 'related'
        email.attach(self._add_header_with_file(self.paths[0]))
        return email

    def get_body(self) -> None:
        self.data.update(
            self._get_name_of_author_of_job_offer() |
            {
                "employee_url": self._get_employee_url(),
                "job_offer_url": self._get_job_offer_url(),
                "image_name": Path(self.paths[0]).name,
                "email": User.get_user_email_by_employee_id(self.data["employee_id"])

            })
        self.body = self.html_form(self.data)

    @get_full_url
    def _get_employee_url(self) -> str:
        """
        The function returns the URL to the profile of the user who applied for the position
        """
        return reverse('employees') + f'?id={self.data["employee_id"]}'

    @get_full_url
    def _get_job_offer_url(self) -> str:
        """
        The function returns the URL to the job offer for which the candidate applied
        """
        return reverse('job-offers') + f'?id={self.data["job_offer_id"]}'

    def _get_name_of_author_of_job_offer(self) -> dict:
        """
        The function returns information about the author of the job offer
        """
        user = User.objects.filter(
            employer__subscription__job_offer=self.data['job_offer_id']).values_list('id', flat=True)[0]
        instance = User.objects.get(id=user)
        return {'first_name': instance.first_name, 'last_name': instance.last_name}


class SendEmailJobOfferMatchmaking(SendEmail):
    """
    Email users who have skills required in a newly added job offer
    """

    def send_email(self):
        self.get_body()
        email = super().send_email()
        email.content_subtype = 'html'
        email.send()

    def _get_obj(self) -> EmailMultiAlternatives:
        email = EmailMultiAlternatives(
            subject=f'New job offer - {self.data["job_offer_title"]}.',
            to=[self.data['email']]
        )
        email.content_subtype = 'html'
        email.attach_alternative(self.body, "text/html")
        email.mixed_subtype = 'related'
        email.attach(self._add_header_with_file(self.paths[0]))
        return email

    def get_body(self) -> None:
        self.data.update(
            self._get_employee_data(self.data['employee']) |
            {
                "url": self._get_job_offer_url(),
                "image_name": Path(self.paths[0]).name
            }
        )
        self.body = self.html_form(self.data)

    @get_full_url
    def _get_job_offer_url(self) -> str:
        """
        The function returns the URL to the job offer for which the candidate applied
        """
        return reverse('job-offers') + f'?id={self.data["job_offer_id"]}'

    @staticmethod
    def _get_employee_data(employee: str) -> dict[str, str]:
        """
        Get user details to display in email header
        """
        instance = User.objects.get(employee=employee)
        return {'first_name': instance.first_name, 'last_name': instance.last_name}
