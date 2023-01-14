from enum import Enum
from decimal import Decimal
from decouple import config
import json


class Standard(Enum):
    """
    The component fields have values for a standard subscription
    """
    PRICE = Decimal(config("STANDARD_PRICE"))
    DAYS = config("STANDARD_DAYS")
    LOCATIONS = config("STANDARD_LOCATIONS")
    OFFER_RAISE = config("STANDARD_OFFER_RAISE")
    PROMOTING = config("STANDARD_PROMOTING")
    CUSTOMER_CARE = config("STANDARD_CUSTOMER_CARE")
    DAYS_FOR_RAISED = json.loads(config("STANDARD_DAYS_FOR_RAISED"))


class Business(Enum):
    """
    The component fields have values for a business subscription
    """
    PRICE = Decimal(config("BUSINESS_PRICE"))
    DAYS = config("BUSINESS_DAYS")
    LOCATIONS = config("BUSINESS_LOCATIONS")
    OFFER_RAISE = config("BUSINESS_OFFER_RAISE")
    PROMOTING = config("BUSINESS_PROMOTING")
    CUSTOMER_CARE = config("BUSINESS_CUSTOMER_CARE")
    DAYS_FOR_RAISED = json.loads(config("BUSINESS_DAYS_FOR_RAISED"))


class Pro(Enum):
    """
    The component fields have values for a Pro subscription
    """
    PRICE = Decimal(config("PRO_PRICE"))
    DAYS = config("PRO_DAYS")
    LOCATIONS = config("PRO_LOCATIONS")
    OFFER_RAISE = config("PRO_OFFER_RAISE")
    PROMOTING = config("PRO_PROMOTING")
    CUSTOMER_CARE = config("PRO_CUSTOMER_CARE")
    DAYS_FOR_RAISED = json.loads(config("PRO_DAYS_FOR_RAISED"))


class Enterprise(Enum):
    """
    The component fields have values for an enterprise subscription
    """
    PRICE = Decimal(config("ENTERPRISE_PRICE"))
    DAYS = config("ENTERPRISE_DAYS")
    LOCATIONS = config("ENTERPRISE_LOCATIONS")
    OFFER_RAISE = config("ENTERPRISE_OFFER_RAISE")
    PROMOTING = config("ENTERPRISE_PROMOTING")
    CUSTOMER_CARE = config("ENTERPRISE_CUSTOMER_CARE")
    DAYS_FOR_RAISED = json.loads(config("ENTERPRISE_DAYS_FOR_RAISED"))
