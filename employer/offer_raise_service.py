from abc import ABC, abstractmethod
from datetime import timedelta, date
from .static import *


class GetRaisedDate(ABC):
    """
    An abstract class for different types of subscriptions
    """
    def __init__(self, first_day: date):
        self.first_day = first_day

    @abstractmethod
    def get_date(self):
        pass


class GetRaisedDateStandard(GetRaisedDate):
    def get_date(self) -> list[date]:
        """
        The function returns a list of days when the offer should be raised for a standard subscription
        """
        return [self.first_day + timedelta(days=counter) for counter in Standard.DAYS_FOR_RAISED.value]


class GetRaisedDateBusiness(GetRaisedDate):
    def get_date(self) -> list[date]:
        """
        The function returns a list of days when the offer should be raised for a business subscription
        """
        return [self.first_day + timedelta(days=counter) for counter in Business.DAYS_FOR_RAISED.value]


class GetRaisedDatePro(GetRaisedDate):
    def get_date(self) -> list[date]:
        """
        The function returns a list of days when the offer should be raised for a pro subscription
        """
        return [self.first_day + timedelta(days=counter) for counter in Pro.DAYS_FOR_RAISED.value]


class GetRaisedDateEnterprise(GetRaisedDate):
    def get_date(self) -> list[date]:
        """
        The function returns a list of days when the offer should be raised for an enterprise subscription
        """
        return [self.first_day + timedelta(days=counter) for counter in Enterprise.DAYS_FOR_RAISED.value]


class GetTheClosestDate:
    """
    A class that performs an algorithm to find the date closest to the raise date
    """
    def __init__(self, raised_dates: GetRaisedDate):
        self.raised_dates = raised_dates.get_date()

    def get_days_from_raised(self) -> int:
        """
        The function returns information when an offer was last raised
        """
        day_difference = date.today() - self.get_closest_date()
        return day_difference.days

    def get_closest_date(self) -> date:
        """
        The function returns the date closest to today's date
        """
        if date.today() in self.raised_dates:
            return date.today()

        if date.today() > self.raised_dates[-1]:
            return self.raised_dates[-1]

        return self.find_closest_date()

    def find_closest_date(self) -> date:
        """
        The function finds the date closest to today's date
        """
        for date_ in self.raised_dates[::-1]:
            if date_ < date.today():
                return date_
