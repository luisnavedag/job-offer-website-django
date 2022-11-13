from rest_framework import serializers
import re


def validate_city(value: str) -> str:
    """Check that the entered value include a correct city name"""
    if not re.match(r"^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$", value):
        raise serializers.ValidationError(f"{value} is not allowed")
    return value
