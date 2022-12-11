from rest_framework import serializers
import re
from employer.models import Employer
from icecream import ic


def validate_city(city: str) -> str:
    """
    Check that the entered city include a correct city name
    """
    if not re.match(r"^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$", city):
        raise serializers.ValidationError(f"{city} is not allowed")
    return city
