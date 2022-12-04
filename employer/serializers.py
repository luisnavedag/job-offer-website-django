from rest_framework import serializers
from .models import Employer, Subscription


class EmployerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employer
        fields = '__all__'


