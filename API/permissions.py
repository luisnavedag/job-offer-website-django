from rest_framework import permissions


class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow creators of an object
    to edit / delete it. Assumes the model instance has a
    `creator` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `creator`.
        return obj.creator == request.user