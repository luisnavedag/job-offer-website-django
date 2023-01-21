from rest_framework.reverse import reverse
from django.core.mail import EmailMultiAlternatives
from api.email_service.email_service import SendEmail
from api.url_service import get_full_url
from pathlib import Path
import datetime


class SendEmailNewUser(SendEmail):
    """
    The class is used to send an email with an activation link for a new user
    """
    def send_email(self):
        self.get_body()
        email = super().send_email()
        email.send()

    def _get_obj(self) -> EmailMultiAlternatives:
        email = EmailMultiAlternatives(
            subject='Activate your account',
            to=[self.data['email']]
        )
        email.content_subtype = 'html'
        email.attach_alternative(self.body, "text/html")
        email.mixed_subtype = 'related'
        email.attach(self._add_header_with_file(self.paths[0]))
        return email

    def get_body(self) -> None:
        self.data.update({
            "url": self._get_registration_link(),
            "image_name": Path(self.paths[0]).name
        })
        self.body = self.html_form(self.data)

    @get_full_url
    def _get_registration_link(self) -> str:
        """
        The function returns the URL that must be clicked to activate the user
        """
        return rf"{reverse('activate_register')}?id={self.data['id']}&expiration_timestamp={self._get_timestamp()}"

    @staticmethod
    def _get_timestamp() -> datetime:
        return datetime.datetime.utcnow().timestamp() + 300000


class SendEmailPasswordReset(SendEmail):
    """
    The class is used to send an email with a reset password token
    """
    def send_email(self):
        self.get_body()
        email = super().send_email()
        email.send()

    def _get_obj(self) -> EmailMultiAlternatives:
        email = EmailMultiAlternatives(subject='Password Reset', to=[self.data['email']])
        email.content_subtype = 'html'
        email.attach_alternative(self.body, "text/html")
        email.mixed_subtype = 'related'
        email.attach(self._add_header_with_file(self.paths[0]))
        return email

    def get_body(self) -> None:
        self.data.update({
            "url": self._get_reset_link(),
            "image_name": Path(self.paths[0]).name
        })
        self.body = self.html_form(self.data)

    @get_full_url
    def _get_reset_link(self) -> str:
        """
        The function returns an url that contains a password reset token
        """
        return rf"{reverse('password_reset:reset-password-request')}?token={self.data['key']}"
