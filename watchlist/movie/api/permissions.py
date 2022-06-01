from rest_framework import permissions


class AnonPermissionOnly(permissions.BasePermission):
    """Allow only anonymous users to access this endpoint"""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class AdminOrReadOnly(permissions.IsAdminUser):
    """Allow admin users to edit data, non-admin users to read"""

    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.is_staff)
        return request.method == "GET" or admin_permission