from django.core.mail import EmailMessage
from rest_framework.reverse import reverse
from abc import ABC, abstractmethod
import datetime


class SendEmail(ABC):
    """
    The base class for sending emails
    """
    def __init__(self, data: dict[any]):
        self.data = data
        self.body = self._get_body()

    @abstractmethod
    def send_email(self) -> EmailMessage:
        """
        Send email. Add additional parameters if required
        """
        return self._get_obj()

    @abstractmethod
    def _get_obj(self):
        """
        Return an e-mail based on which you can send an e-mail
        """
        pass

    @abstractmethod
    def _get_body(self):
        """
        Enter your email body information
        """
        pass


class SendEmailNewUser(SendEmail):
    """
    The class is used to send an email with an activation link for a new user
    """
    def send_email(self):
        email = super().send_email()
        email.content_subtype = 'html'
        email.send()

    def _get_obj(self) -> EmailMessage:
        return EmailMessage('Activate your account', self.body, to=[self.data['email']])

    def _get_body(self) -> str:
        url = f"{reverse('activate_register')}?id={self.data['id']}&timestamp={self._get_timestamp()}"
        return f'''\
        <html>
        <body>
            <div style="font-family:Consolas;margin:auto 100px;padding:5px;text-size:16px;color:white;background-color:grey">
                <h1>Hello {self.data['username']}!</h1> 
                <h2>Click to activate account: {url}</h2>
            </div>            
        </body>
        </html>
        '''

    @staticmethod
    def _get_timestamp() -> datetime:
        return datetime.datetime.utcnow().timestamp() + 300000


class SendEmailPasswordReset(SendEmail):
    """
    The class is used to send an email with a link to reset the user's password
    """
    def send_email(self):
        email = super().send_email()
        email.content_subtype = 'html'
        email.send()

    def _get_obj(self) -> EmailMessage:
        return EmailMessage('Password Reset', self.body, to=[self.data['email']])

    def _get_body(self) -> str:
        url = f"{reverse('password_reset:reset-password-request')}?token={self.data['key']}"
        return f'''\
        <html>
        <body>
            <div style="font-family:Consolas;margin:auto 100px;padding:5px;text-size:16px;color:white;background-color:grey">
                <h1>Hello {self.data['username']}!</h1> 
                <h2>We’ve received a request to reset the password for the Website account associated
                 with {self.data['email']}. No changes have been made to your account yet.
                 </h2>
                <h2>Click to reset your password: {url}</h2>
            </div>            
        </body>
        </html>
        '''
