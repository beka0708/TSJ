from rest_framework import permissions
from apps.user.models import CustomUser


class IsManagerOrOwnerOrTenant(permissions.BasePermission):

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        allowed_roles = {CustomUser.MANAGER, CustomUser.OWNER, CustomUser.TENANT}
        return request.user.role in allowed_roles

