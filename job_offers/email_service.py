from user.email_service import SendEmail
from django.core.mail import EmailMessage
from rest_framework.reverse import reverse
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
