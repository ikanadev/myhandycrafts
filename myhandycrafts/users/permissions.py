"""User permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_permission(self,request,view):
        """Check obj and user are the same."""
        return request.user.is_staff