from django.db.models.signals import post_delete
from employee.models import Employee
from django.dispatch import receiver


@receiver(post_delete, sender=Employee)
def delete_user(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

