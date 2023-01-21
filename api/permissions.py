from rest_framework import permissions
from employer.models import Employer
from employee.models import Employee
from user.models import User


class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Verify that the user requesting access to the resource is its author
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsEmployer(permissions.BasePermission):
    """
    Verify that the user requesting access to the resource is an employer
    """
    def has_permission(self, request, view):
        return Employer.objects.filter(user=request.user).exists()


class IsEmployee(permissions.BasePermission):
    """
    Verify that the user requesting access to the resource is an employee
    """
    def has_permission(self, request, view):
        return Employee.objects.filter(user=request.user).exists()


class IsJobOfferCreator(permissions.BasePermission):
    """
    Check if the user who wants to update a given subscription is its author
    """
    def has_object_permission(self, request, view, obj):
        return User.objects.get(employer__subscription__job_offer=obj.id) == request.user
