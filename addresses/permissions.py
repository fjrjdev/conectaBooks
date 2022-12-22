from rest_framework import permissions
import ipdb


class isOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if obj.user.id == request.user.id:
            return True
