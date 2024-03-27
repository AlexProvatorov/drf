from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение при котором доступ имеет только админ, остальные могут выполнять
    только SAFE_METHODS.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsOwnerUser(permissions.BasePermission):
    """
    Разрешение при котором доступ имеет только владелец.
    """
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user
