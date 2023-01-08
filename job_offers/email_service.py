from user.email_service import SendEmail
from django.core.mail import EmailMessage
from rest_framework.reverse import reverse
from user.models import User
import datetime


class SendEmailJobOfferVerification(SendEmail):
    """
    The class is used to send an e-mail to the admin to check the correctness of the entered data
    """

    def send_email(self):
        email = super().send_email()
        email.content_subtype = 'html'
        email.send()

    def _get_obj(self) -> EmailMessage:
        return EmailMessage(
            f'Verification of the job offer - {self.data["title"]}', self.body, to=('test.grzegorzp@gmail.com',)
        )

    def _get_body(self) -> str:
        url = reverse('job_offer_verification', kwargs={'pk': self.data['id']})
        url = f"{url}?title={self.data['title']}&expiration_timestamp={self._get_timestamp()}"
        return f'''\
        <html>
        <body>
            <div style="font-family:Consolas;margin:auto 100px;padding:5px;text-size:16px;color:white;background-color:grey">
                <h1>Verification of the job offer</h1> 
                <h2>Please verify that the offer below does not contain any prohibited elements</h2>
                <div>
                <p>{self.data['title']}</p>
                <p>{self.data['job_description']}</p>
                <p>{self.data['address']}</p>
                <p>{self.data['information_clause']}</p>
                <p>{self.data['contact_name']}</p>
                <p>{self.data['contact_email']}</p>
                <p>{self.data['contact_phone']}</p>
                </div>
                <div>
                If the above job offer is correct, please click on the link below
                </div>
                <a href="{url}" target="_blank">Click here</a>
            </div>            
        </body>
        </html>
        '''

    @staticmethod
    def _get_timestamp() -> datetime:
        return datetime.datetime.utcnow().timestamp() + 86400000


class SendEmailJobOfferNewApplication(SendEmail):

    def send_email(self):
        email = super().send_email()
        email.content_subtype = 'html'
        email.send()

    def _get_obj(self) -> EmailMessage:
        return EmailMessage(
            f'The application for your job offer - {self.data["job_offer_title"]}, has just been submitted!',
            self.body,
            to=('test.grzegorzp@gmail.com',) #todo usun email
        )

    def _get_body(self) -> str:
        employer = self._get_name_of_author_of_job_offer()
        return f'''\
        <html>
        <body>
            <div style="font-family:Consolas;margin:auto 100px;padding:5px;text-size:16px;color:white;background-color:grey">
                <h1>Application for the position - {self.data["job_offer_title"]}</h1> 
                <h2>Hi {employer['first_name']} {employer['last_name']}</h2>
                <h2>Someone just applied for one of your job offers!</h2>
                
                <div>
                To go to the profile of the candidate for the position you are applying for, click on the link below:
                </div>
                <a href="{self._get_employee_url()}" target="_blank">Click here</a>
                <div>
                To go to the job offer, click on the link below:
                </div>
                <a href="{self._get_employee_url()}" target="_blank">Click here</a>
            </div>            
        </body>
        </html>
        '''

    def _get_employee_url(self) -> str:
        """
        The function returns the URL to the profile of the user who applied for the position
        """
        return reverse('employees') + f'?id={self.data["employee_id"]}'

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
