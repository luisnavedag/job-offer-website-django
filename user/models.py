import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from .email_service import SendEmailPasswordReset


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.email


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    The function via signals send an email with a link to reset the password
    """
    SendEmailPasswordReset({
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        "key": reset_password_token.key
    }).send_email()
