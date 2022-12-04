from django.db.models.signals import post_delete
from employer.models import Employer
from django.dispatch import receiver


@receiver(post_delete, sender=Employer)
def delete_user(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

