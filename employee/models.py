from django.db import models
from django.conf import settings
from general_utils.models import CommonItem


class Employee(models.Model):
    STATUS = (
        ("Active", "I'm actively looking for a job"),
        ("Open", "Open for proposals"),
        ("Closed", "Not open for proposals"),
    )

    TAGS = (
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Finances', 'Finances'),
        ('Engineering', 'Engineering'),
        ('Design', 'Design'),
        ('HR', 'HR'),
        ('Consulting', 'Consulting'),
        ('BI-&-Data', 'BI & Data'),
        ('SEO', 'SEO'),
        ('PM', 'PM'),
        ('Media', 'Media'),
        ('Support', 'Support'),
        ('Logistic', 'Logistic'),
        ('Other', 'Other'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    skills = models.ManyToManyField('Skill', blank=True)
    tags = models.CharField(choices=TAGS, max_length=100, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    linkdin = models.URLField(max_length=200, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    about_yourself = models.TextField(null=True, blank=True)
    accept_matchmaking = models.BooleanField(default=False)

    def __str__(self):
        return self.user


class Skill(CommonItem):
    pass
