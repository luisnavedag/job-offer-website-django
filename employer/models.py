from django.db import models
from django.conf import settings
from datetime import date, timedelta
from django.contrib.auth.models import AbstractUser


class Employer(models.Model):
    USER = settings.AUTH_USER_MODEL

    user = models.ForeignKey(USER, default=1, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_size = models.IntegerField(default=0)
    website = models.CharField(max_length=200)

    class Meta:
        unique_together = [['website', 'user']]


class Subscription(models.Model):
    employer = models.ForeignKey(Employer, default=1, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    days = models.IntegerField(default=30)
    locations = models.IntegerField(default=1)
    offer_raise = models.IntegerField(default=1)
    promoting = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    first_day = models.DateTimeField(auto_now_add=True)
    # last_day = models.DateField(default=date.today() + timedelta(30)) signals
