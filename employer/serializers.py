from rest_framework import serializers
from .models import Employer, Subscription, Payment
from user.models import User
from .static import *
from datetime import timedelta, date
from job_offers.models import JobOffer
from django.db import transaction


class EmployerSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()

    class Meta:
        model = Employer
        fields = '__all__'

    def get_user(self, obj) -> User:
        return User.objects.get(email=obj.user).id


class SubscriptionSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Subscription
        fields = [
            'id',
            'employer',
            'payment',
            'job_offer',
            'type',
            'days',
            'locations',
            'offer_raise',
            'promoting',
            'customer_care',
            'created',
            'first_day',
            'last_day',
        ]

    @transaction.atomic
    def create(self, validated_data: dict) -> Subscription:
        type_obj = self._get_enum(validated_data['type'])

        employer = Employer.objects.get(user=validated_data['user'])

        payment = Payment.objects.create(
            amount=type_obj.PRICE.value,
            status='UNPAID'
        )

        job_offer = JobOffer.objects.create()
        last_day = validated_data['first_day'] + timedelta(days=30)

        instance = Subscription.objects.create(
            employer=employer,
            payment=payment,
            job_offer=job_offer,
            type=validated_data['type'],
            days=type_obj.DAYS.value,
            locations=type_obj.LOCATIONS.value,
            offer_raise=type_obj.OFFER_RAISE.value,
            promoting=type_obj.PROMOTING.value,
            customer_care=type_obj.CUSTOMER_CARE.value,
            first_day=validated_data['first_day'],
            last_day=last_day
        )
        return instance

    def validate_first_day(self, value: date) -> date:
        if value < date.today():
            raise serializers.ValidationError("The first day of displaying the offer cannot be less than today's date")
        if value > date.today() + timedelta(days=60):
            raise serializers.ValidationError("The first day of displaying the offer cannot be longer than 2 months")
        return value

    @staticmethod
    def _get_enum(ad_type: str) -> type(Enum):
        match ad_type:
            case 'Standard':
                return Standard
            case 'Business':
                return Business
            case 'Pro':
                return Pro
            case 'Enterprise':
                return Enterprise
