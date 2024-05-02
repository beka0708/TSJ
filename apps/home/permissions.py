from rest_framework import permissions
from apps.user.models import CustomUser


class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):

        return request.user and request.user.is_authenticated and request.user.role == CustomUser.MANAGER
