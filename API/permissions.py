from rest_framework import permissions
from employer.models import Employer


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return Employer.objects.filter(user=request.user).exists()

