from rest_framework import permissions


class AdminOrReadOnly(permissions.IsAdminUser):
    """Allow admin users to edit data, non-admin users to read"""

    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.is_staff)
        return request.method == "GET" or admin_permission


class ReviewUserOrReadOnly(permissions.BasePermission):
    """Allow users to edit their own reviews, non-users to read"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Read permissions are allowed to any request,
            return True

        return obj.user == request.user
