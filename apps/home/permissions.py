from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет только администраторам редактировать объекты.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == "ADMIN"


class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет только менеджерам редактировать объекты.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == "MANAGER"


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, которое позволяет только владельцам редактировать объекты.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
