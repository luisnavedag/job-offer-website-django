from enum import Enum
from decimal import Decimal


class Standard(Enum):
    """
    The component fields have values for a standard subscription
    """
    PRICE = Decimal('100')
    DAYS = 30
    LOCATIONS = 1
    OFFER_RAISE = 1
    PROMOTING = False
    CUSTOMER_CARE = False


class Bussiness(Enum):
    """
    The component fields have values for a business subscription
    """
    PRICE = Decimal('140')
    DAYS = 30
    LOCATIONS = 2
    OFFER_RAISE = 2
    PROMOTING = True
    CUSTOMER_CARE = False


class Pro(Enum):
    """
    The component fields have values for a Pro subscription
    """
    PRICE = Decimal('200')
    DAYS = 30
    LOCATIONS = 5
    OFFER_RAISE = 3
    PROMOTING = True
    CUSTOMER_CARE = True


class Enterprise(Enum):
    """
    The component fields have values for an enterprise subscription
    """
    PRICE = Decimal('290')
    DAYS = 30
    LOCATIONS = 19
    OFFER_RAISE = 5
    PROMOTING = True
    CUSTOMER_CARE = True
