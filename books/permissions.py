from rest_framework import permissions
from utils.validation_error import CustomForbidenError


class IsAdmOrOwnerBook(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.id == obj.user_id or request.user.is_superuser
