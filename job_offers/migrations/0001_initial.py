# Generated by Django 4.1.5 on 2023-01-22 15:29

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('tags', models.CharField(choices=[('Marketing', 'Marketing'), ('Sales', 'Sales'), ('Finances', 'Finances'), ('Engineering', 'Engineering'), ('Design', 'Design'), ('HR', 'HR'), ('Consulting', 'Consulting'), ('BI-&-Data', 'BI & Data'), ('SEO', 'SEO'), ('PM', 'PM'), ('Media', 'Media'), ('Support', 'Support'), ('Logistic', 'Logistic'), ('Other', 'Other')], max_length=100)),
                ('experience', models.CharField(choices=[('Internship/Junior', 'Internship/Junior'), ('Mid', 'Mid'), ('Senior', 'Senior'), ('Manager/C-level', 'Manager/C level')], max_length=100)),
                ('form_of_employment', models.CharField(choices=[('Fixed-term-contract', 'Fixed-term contract'), ('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Self-employment', 'Self-employment'), ('Internship-employment', 'Internship employment')], max_length=100)),
                ('salary_from', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('salary_up_to', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('currency', models.CharField(blank=True, choices=[('GBP', 'GBP'), ('EUR', 'EUR'), ('CHF', 'CHF'), ('USD', 'USD'), ('PLN', 'PLN')], max_length=100)),
                ('job_description', models.TextField()),
                ('address', models.CharField(max_length=200)),
                ('operationg_mode', models.CharField(choices=[('Remote-work', 'Remote work'), ('Hybrid-work', 'Hybrid work'), ('On-site', 'On site')], max_length=100)),
                ('working_time', models.CharField(choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Internship', 'Internship')], max_length=100)),
                ('remote_recruitment', models.BooleanField(blank=True, null=True)),
                ('information_clause', models.CharField(max_length=500)),
                ('employee_clause', models.BooleanField(default=False)),
                ('contact_name', models.CharField(max_length=200)),
                ('contact_email', models.EmailField(max_length=200)),
                ('contact_phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('verified', models.BooleanField(default=False)),
                ('activated', models.BooleanField(default=False)),
                ('cities', models.ManyToManyField(to='job_offers.city')),
                ('skills', models.ManyToManyField(blank=True, to='employee.skill')),
                ('skills_nice_to_have', models.ManyToManyField(blank=True, related_name='skills_nice_to_have', to='employee.skill')),
            ],
        ),
        migrations.CreateModel(
            name='Matchmaking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
                ('job_offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_offers.joboffer')),
            ],
            options={
                'unique_together': {('employee', 'job_offer')},
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
                ('job_offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_offers.joboffer')),
            ],
            options={
                'unique_together': {('employee', 'job_offer')},
            },
        ),
    ]
