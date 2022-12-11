from rest_framework import serializers
from .models import Employer, Subscription
from user.models import User
from icecream import ic


class EmployerSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()

    class Meta:
        model = Employer
        fields = '__all__'

    def get_user(self, obj):
        return User.objects.get(email=obj.user).id
