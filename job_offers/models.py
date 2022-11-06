from django.db import models
from employer.models import Subscription
from phonenumber_field.modelfields import PhoneNumberField
from employee.models import Skill


class JobOffer(models.Model):
    TAGS = (
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Finances', 'Finances'),
        ('Engineering', 'Engineering'),
        ('Design', 'Design'),
        ('HR', 'HR'),
        ('Consulting', 'Consulting'),
        ('BI & Data', 'BI & Data'),
        ('SEO', 'SEO'),
        ('PM', 'PM'),
        ('Media', 'Media'),
        ('Support', 'Support'),
        ('Logistic', 'Logistic'),
        ('Other', 'Other'),
    )

    EXPERIENCE = (
        ('Internship/Junior', 'Internship/Junior'),
        ('Mid', 'Mid'),
        ('Senior', 'Senior'),
        ('Manager/C level', 'Manager/C level'),
    )

    FORM_OF_EMPLOYMENT = (
        ('Fixed-term contract', 'Fixed-term contract'),
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Self-employment', 'Self-employment'),
        ('Internship employment', 'Internship employment'),
    )

    CURRENCY = (
        ('GBP', 'GBP'),
        ('EUR', 'EUR'),
        ('CHF', 'CHF'),
        ('USD', 'USD'),
        ('PLN', 'PLN'),
    )

    OPERATING_MODE = (
        ('Remote work', 'Remote work'),
        ('Hybrid work', 'Hybrid work'),
        ('On site', 'On site'),
    )

    WORKING_TIME = (
        ('Full time', 'Full time'),
        ('Part time', 'Part time'),
        ('Internship', 'Internship'),
    )

    subscription = models.ForeignKey(Subscription, null=True, on_delete=models.SET_NULL)
    skills = models.ManyToManyField('employee.Skill', blank=True)
    skills_nice_to_have = models.ManyToManyField('employee.Skill', blank=True, related_name='skills_nice_to_have')
    tags = models.CharField(choices=TAGS, max_length=100)
    workplace = models.CharField(max_length=100)
    experience = models.CharField(choices=EXPERIENCE, max_length=100)
    form_of_employment = models.CharField(choices=FORM_OF_EMPLOYMENT, max_length=100)
    salary_from = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    salary_up_to = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    currency = models.CharField(choices=CURRENCY, max_length=100)
    job_description = models.TextField()
    city = models.CharField(max_length=200)
    addres = models.CharField(max_length=200)
    operationg_mode = models.CharField(choices=OPERATING_MODE, max_length=100)
    working_time = models.CharField(choices=WORKING_TIME, max_length=100)
    remote_recruitment = models.BooleanField(null=True, blank=True)
    information_clause = models.CharField(max_length=500)
    employee_clause = models.BooleanField(default=False)
    contact_name = models.CharField(max_length=200)
    contact_email = models.EmailField(max_length=200)
    contact_phone = PhoneNumberField(null=True, blank=True)
    # offer_paid_off
    created = models.DateTimeField(auto_now_add=True)



