from django.db import models
from django.conf import settings


class Employee(models.Model):
    USER = settings.AUTH_USER_MODEL
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
        ('BI & Data', 'BI & Data'),
        ('SEO', 'SEO'),
        ('PM', 'PM'),
        ('Media', 'Media'),
        ('Support', 'Support'),
        ('Logistic', 'Logistic'),
        ('Other', 'Other'),
    )

    user = models.ForeignKey(USER, default=1, on_delete=models.CASCADE)
    skills = models.ManyToManyField('Skill', blank=True)
    tags = models.CharField(choices=TAGS, max_length=100)
    city = models.CharField(max_length=200, null=True, blank=True)
    linkdin = models.URLField(max_length=200, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100)
    about_yourself = models.TextField(null=True, blank=True)


class Skill(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)


