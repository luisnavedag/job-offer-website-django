from rest_framework import serializers
from .models import Employer, Subscription, Payment
from user.models import User
from .static import *
from datetime import timedelta
from icecream import ic


class EmployerSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()

    class Meta:
        model = Employer
        fields = '__all__'

    def get_user(self, obj):
        return User.objects.get(email=obj.user).id


class SubscriptionSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Subscription
        fields = [
            'id',
            'employer',
            'payment',
            'type', #
            'days',
            'locations',
            'offer_raise',
            'promoting',
            'customer_care',
            'created',
            'first_day', #
            'last_day',
        ]

    def create(self, validated_data):
        type_obj = self._get_enum(validated_data['type'])
        employer = Employer.objects.get(user=validated_data['user'])
        payment = Payment.objects.create(
            amount=type_obj.PRICE.value,
            status='UNPAID'
        )
        last_day = validated_data['first_day'] + timedelta(days=30)
        return Subscription.objects.create(
            employer=employer,
            payment=payment,
            type=validated_data['type'],
            days=type_obj.DAYS.value,
            locations=type_obj.LOCATIONS.value,
            offer_raise=type_obj.OFFER_RAISE.value,
            promoting=type_obj.PROMOTING.value,
            customer_care=type_obj.CUSTOMER_CARE.value,
            first_day=validated_data['first_day'],
            last_day=last_day
        )

    @staticmethod
    def _get_enum(ad_type: str):
        match ad_type:
            case 'Standard':
                return Standard
            case 'Bussiness':
                return Bussiness
            case 'PRO':
                return Pro
            case 'Enterprise':
                return Enterprise
