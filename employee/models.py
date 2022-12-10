from django.db import models
from django.conf import settings
# from user.models import User
# from django.contrib.auth.models import User

class Employee(models.Model):
    # USER = get_user_model()
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

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    skills = models.ManyToManyField('Skill', blank=True)
    tags = models.CharField(choices=TAGS, max_length=100, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    linkdin = models.URLField(max_length=200, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    about_yourself = models.TextField(null=True, blank=True)


class Skill(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)

