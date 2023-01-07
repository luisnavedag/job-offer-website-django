from rest_framework import serializers
from job_offers.models import JobOffer, City
from employee.serializers import SkillSerializer
from employee.models import Skill
from django.db.models import Model
from .email_service import SendEmailJobOfferVerification
from employer.offer_raise_service import *
from itertools import product
from employer.models import Subscription


class CitySerializer(serializers.ModelSerializer):

    name = serializers.CharField()

    class Meta:
        model = City
        fields = [
            'name'
        ]


class JobOfferSerializer(serializers.ModelSerializer):

    skills = SkillSerializer(many=True, required=False)
    skills_nice_to_have = SkillSerializer(many=True, required=False)
    cities = CitySerializer(many=True, required=True)

    class Meta:
        model = JobOffer
        fields = [
            'id',
            'skills',
            'skills_nice_to_have',
            'cities',
            'title',
            'tags',
            'experience',
            'form_of_employment',
            'salary_from',
            'salary_up_to',
            'currency',
            'job_description',
            'address',
            'operationg_mode',
            'working_time',
            'remote_recruitment',
            'information_clause',
            'employee_clause',
            'contact_name',
            'contact_email',
            'contact_phone',
        ]

    def update(self, instance: JobOffer, validated_data: dict) -> JobOffer:

        if validated_data.get('skills', None):
            instance.skills.clear()
            instance.skills.add(*self._create_obj_name_field('skills', validated_data, Skill))

        if validated_data.get('skills_nice_to_have', None):
            instance.skills_nice_to_have.clear()
            instance.skills_nice_to_have.add(*self._create_obj_name_field('skills_nice_to_have', validated_data, Skill))

        if validated_data.get('cities', None):
            instance.cities.clear()
            instance.cities.add(*self._create_obj_name_field('cities', validated_data, City))

        instance.title = validated_data.get('title', instance.title)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.form_of_employment = validated_data.get('form_of_employment', instance.form_of_employment)
        instance.salary_from = validated_data.get('salary_from', instance.salary_from)
        instance.salary_up_to = validated_data.get('salary_up_to', instance.salary_up_to)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.job_description = validated_data.get('job_description', instance.job_description)
        instance.address = validated_data.get('address', instance.address)
        instance.operationg_mode = validated_data.get('operationg_mode', instance.operationg_mode)
        instance.working_time = validated_data.get('working_time', instance.working_time)
        instance.remote_recruitment = validated_data.get('remote_recruitment', instance.remote_recruitment)
        instance.information_clause = validated_data.get('information_clause', instance.information_clause)
        instance.employee_clause = validated_data.get('employee_clause', instance.employee_clause)
        instance.contact_name = validated_data.get('contact_name', instance.contact_name)
        instance.contact_email = validated_data.get('contact_email', instance.contact_email)
        instance.contact_phone = validated_data.get('contact_phone', instance.contact_phone)
        instance.activated = validated_data.get('activated', instance.activated)
        instance.verified = False

        instance.save()

        SendEmailJobOfferVerification(instance.__dict__).send_email()

        return instance

    def validate(self, data: dict) -> dict:
        """
        Validation checking the following data:
        - the number of entered cities cannot be greater than the number of cities purchased in the subscription
        - the same skill cannot be in the skills and skills_nice_to_have fields
        """
        if Subscription.objects.get(job_offer=self.instance.id).locations < len(data.get('cities', '')):
            raise serializers.ValidationError(
                'The number of cities cannot be greater than the number of locations in the subscription.'
            )

        if data.get('skills', None) and data.get('skills_nice_to_have', None) and self._validation_of_unique_skills(data):
            raise serializers.ValidationError(
                'Skills and skills nice to have cannot contain the same elements.'
            )

        return data

    @staticmethod
    def _validation_of_unique_skills(data: dict) -> bool:
        """
        The function checks if skills and skills_nice_to_have have the same elements
        """
        skills = [skill['name'] for skill in data['skills']]
        skills_nice_to_have = [skill['name'] for skill in data['skills_nice_to_have']]
        return any([True if items[0] == items[1] else False for items in list(product(skills, skills_nice_to_have))])

    @staticmethod
    def _create_obj_name_field(name: str, validated_data: dict, obj: Model) -> tuple:
        """
        Create tuples of objects that can be assigned to any field in a many-to-many relationship
        """
        instances = []
        items = validated_data.pop(name)
        for item in items:
            instance, _ = obj.objects.get_or_create(name=item['name'])
            instance.save()
            instances.append(instance)
        return tuple(instances)


class JobOfferFilterSerializer(JobOfferSerializer):

    days_to_raise = serializers.SerializerMethodField()

    class Meta:
        model = JobOffer
        fields = '__all__'

    def get_days_to_raise(self, obj):
        """
        The days_to_raise field will be created accordingly before sending the request
        """
        subscription_obj = Subscription.objects.get(id=obj.id)

        match subscription_obj.type:
            case 'Standard':
                return GetTheClosestDate(GetRaisedDateStandard(subscription_obj.first_day)).get_days_from_raised()
            case 'Business':
                return GetTheClosestDate(GetRaisedDateBusiness(subscription_obj.first_day)).get_days_from_raised()
            case 'Pro':
                return GetTheClosestDate(GetRaisedDatePro(subscription_obj.first_day)).get_days_from_raised()
            case 'Enterprise':
                return GetTheClosestDate(GetRaisedDateEnterprise(subscription_obj.first_day)).get_days_from_raised()
