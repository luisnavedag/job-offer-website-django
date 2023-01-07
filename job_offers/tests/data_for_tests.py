import pytest
from job_offers.models import JobOffer, City
from employer.models import Employer, Subscription, Payment
from datetime import date, timedelta
from employer.static import *


@pytest.mark.django_db
def create_subs(
        create_employer: Employer,
        subs_type: type[Standard | Pro | Business | Enterprise],
        first_day: date,
        job_offer: JobOffer) -> Subscription:
    """
    The function adds subscriptions to the database and returns an object
    """
    return Subscription.objects.create(
        employer=create_employer,
        payment=Payment.objects.create(),
        job_offer=job_offer,
        type=subs_type.__name__,
        days=subs_type.DAYS.value,
        locations=subs_type.LOCATIONS.value,
        offer_raise=subs_type.OFFER_RAISE.value,
        promoting=subs_type.PROMOTING.value,
        customer_care=subs_type.CUSTOMER_CARE.value,
        created=date.today(),
        first_day=first_day,
        last_day=first_day + timedelta(days=30)
    )


def create_obj_name_field(items: list, obj: type[City]) -> tuple:
    """
    Create tuples of objects that can be assigned to any field in a many-to-many relationship
    """
    instances = []
    for item in items:
        instance, _ = obj.objects.get_or_create(name=item['name'])
        instance.save()
        instances.append(instance)
    return tuple(instances)


@pytest.mark.django_db
def create_job_offer(
        title: str, cities: list, tags: str, experience: str, form_of_employment: str,
        salary_from: int, salary_up_to: int, operationg_mode: str, working_time: str):
    """
    The function adds job offer to the database and returns an object
    """
    instance = JobOffer.objects.create(
        title=title,
        tags=tags,
        experience=experience,
        form_of_employment=form_of_employment,
        salary_from=salary_from,
        salary_up_to=salary_up_to,
        currency='GBP',
        job_description='Lorem Ipsum is simply dummy text of the printing',
        address='Cracow, Rynek',
        operationg_mode=operationg_mode,
        working_time=working_time,
        remote_recruitment=True,
        information_clause='Lorem Ipsum is simply dummy text of the printing',
        employee_clause=True,
        contact_name='John Doe',
        contact_email='johndoe@op.pl',
        contact_phone='+48502502502',
        verified=True)

    instance.cities.add(*create_obj_name_field(cities, City))

    return instance


@pytest.fixture
def create_data(create_employer: Employer) -> list:
    """
    Creating data in the database for testing purposes
    """
    return[
        create_subs(create_employer, Pro, get_date(0), create_job_offer(
            title='Python Programer',
            cities=[{'name': 'Cracow'}, {'name': 'Lodz'}, {'name': 'Gdansk'}, {'name': 'Lublin'}, {'name': 'Sopot'}],
            tags='Engineering',
            experience='Mid',
            form_of_employment='Full-time',
            salary_from=2000,
            salary_up_to=3000,
            operationg_mode='Remote-work',
            working_time='Full-time'
        )),
        create_subs(create_employer, Business, get_date(16), create_job_offer(
            title='SEM Planner',
            cities=[{'name': 'Cracow'}, {'name': 'Sopot'}],
            tags='Marketing',
            experience='Senior',
            form_of_employment='Self-employment',
            salary_from=2300,
            salary_up_to=3200,
            operationg_mode='Remote-work',
            working_time='Full-time'
        )),
        create_subs(create_employer, Standard, get_date(4), create_job_offer(
            title='Graphic Design Intern',
            cities=[{'name': 'Cracow'}],
            tags='Design',
            experience='Internship/Junior',
            form_of_employment='Internship-employment',
            salary_from=0,
            salary_up_to=0,
            operationg_mode='On-site',
            working_time='Internship'
        )),
        create_subs(create_employer, Pro, get_date(9), create_job_offer(
            title='Recruitment Specialist',
            cities=[{'name': 'Cracow'}, {'name': 'Lodz'}, {'name': 'Gdansk'}, {'name': 'Lublin'}, {'name': 'Sopot'}],
            tags='HR',
            experience='Senior',
            form_of_employment='Self-employment',
            salary_from=1800,
            salary_up_to=2500,
            operationg_mode='Remote-work',
            working_time='Full-time'
        )),
        create_subs(create_employer, Business, get_date(17), create_job_offer(
            title='Data Analyst',
            cities=[{'name': 'Gliwice'}, {'name': 'Katowice'}],
            tags='Finances',
            experience='Mid',
            form_of_employment='Fixed-term-contract',
            salary_from=2200,
            salary_up_to=2600,
            operationg_mode='Hybrid-work',
            working_time='Part-time'
        )),
        create_subs(create_employer, Business, get_date(20), create_job_offer(
            title='Cardo Operations Manager',
            cities=[{'name': 'Gdansk'}, {'name': 'Sopot'}],
            tags='Logistic',
            experience='Manager/C-level',
            form_of_employment='Self-employment',
            salary_from=4000,
            salary_up_to=5000,
            operationg_mode='Hybrid-work',
            working_time='Full-time'
        )),
        create_subs(create_employer, Enterprise, get_date(0), create_job_offer(
            title='Java Programmer',
            cities=[{'name': 'Cracow'}, {'name': 'Lodz'}, {'name': 'Gdansk'}, {'name': 'Lublin'},
                    {'name': 'Sopot'}, {'name': 'Radom'}, {'name': 'Gliwice'}, {'name': 'Sosnowiec'},
                    {'name': 'Szczecin'}, {'name': 'Kielce'}, {'name': 'Zamosc'}, {'name': 'Krynica'},
                    {'name': 'Nowy Sacz'}, {'name': 'Skawina'}, {'name': 'Rzeszow'}, {'name': 'Zielona-Gora'},
                    {'name': 'Elblag'}, {'name': 'Poznan'}, {'name': 'Warszawa'}],
            tags='Engineering',
            experience='Senior',
            form_of_employment='Full-time',
            salary_from=3500,
            salary_up_to=5000,
            operationg_mode='Remote-work',
            working_time='Full-time'
        )),
        create_subs(create_employer, Pro, get_date(3), create_job_offer(
            title='Administrative Assistant',
            cities=[{'name': 'Cracow'}, {'name': 'Lodz'}, {'name': 'Gdansk'}, {'name': 'Lublin'}, {'name': 'Sopot'}],
            tags='HR',
            experience='Internship/Junior',
            form_of_employment='Full-time',
            salary_from=1200,
            salary_up_to=1400,
            operationg_mode='Remote-work',
            working_time='Full-time'
        )),
        create_subs(create_employer, Standard, get_date(16), create_job_offer(
            title='Electrical Designer',
            cities=[{'name': 'Bydgoszcz'}],
            tags='Engineering',
            experience='Internship/Junior',
            form_of_employment='Part-time',
            salary_from=800,
            salary_up_to=1000,
            operationg_mode='On-site',
            working_time='Part-time'
        )),
        create_subs(create_employer, Enterprise, get_date(9), create_job_offer(
            title='Graphic Designer',
            cities=[{'name': 'Cracow'}, {'name': 'Bielsko-Biala'}, {'name': 'Gdansk'}, {'name': 'Lublin'},
                    {'name': 'Sopot'}, {'name': 'Radom'}, {'name': 'Gliwice'}, {'name': 'Sosnowiec'},
                    {'name': 'Szczecin'}, {'name': 'Kielce'}, {'name': 'Zamosc'}, {'name': 'Krynica'},
                    {'name': 'Nowy Sacz'}, {'name': 'Skawina'}, {'name': 'Rzeszow'}, {'name': 'Zielona-Gora'},
                    {'name': 'Elblag'}, {'name': 'Poznan'}, {'name': 'Warszawa'}],
            tags='Design',
            experience='Mid',
            form_of_employment='Full-time',
            salary_from=1700,
            salary_up_to=2200,
            operationg_mode='Hybrid-work',
            working_time='Full-time'
        )),
        create_subs(create_employer, Standard, get_date(-1), create_job_offer(
            title='Controls Engineer',
            cities=[{'name': 'Torun'}],
            tags='Engineering',
            experience='Internship/Junior',
            form_of_employment='Part-time',
            salary_from=300,
            salary_up_to=6000,
            operationg_mode='On-site',
            working_time='Part-time'
        )),
        create_subs(create_employer, Standard, get_date(31), create_job_offer(
            title='Electronic System Engineer',
            cities=[{'name': 'Cracow'}],
            tags='Engineering',
            experience='Mid',
            form_of_employment='Self-employment',
            salary_from=3000,
            salary_up_to=4000,
            operationg_mode='On-site',
            working_time='Full-time'
        )),
    ]


def get_date(value: int) -> date:
    """
    Create a back date based on today's date for testing purposes
    """
    return date.today() - timedelta(days=value)
