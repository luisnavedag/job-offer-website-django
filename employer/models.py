from django.db import models
from django.conf import settings
from job_offers.models import JobOffer


class Employer(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    company_name = models.CharField(max_length=200)
    company_size = models.IntegerField(default=0)
    website = models.URLField(max_length=200)

    class Meta:
        unique_together = ['website', 'user']


class Payment(models.Model):
    STATUS = (
        ("UNPAID", "UNPAID"),
        ("IN PROGRESS", "IN PROGRESS"),
        ("PAID", "PAID"),
    )

    amount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(choices=STATUS, max_length=100, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Subscription(models.Model):

    TYPE = (
        ("Standard", "Standard"),
        ("Business", "Business"),
        ("Pro", "Pro"),
        ("Enterprise", "Enterprise"),
    )

    employer = models.ForeignKey(Employer, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    job_offer = models.ForeignKey(JobOffer, on_delete=models.SET_NULL, blank=True, null=True)
    type = models.CharField(choices=TYPE, max_length=100)
    days = models.IntegerField(default=30)
    locations = models.IntegerField(default=1)
    offer_raise = models.IntegerField(default=1)
    promoting = models.BooleanField(default=False)
    customer_care = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    first_day = models.DateField()
    last_day = models.DateField(blank=True)


