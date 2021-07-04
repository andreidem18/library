from rest_framework.permissions import BasePermission

class GeneralPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH'] and not request.user.is_authenticated:
            return False
        if request.method == 'DELETE' and not request.user.is_staff:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['POST', 'PUT', 'PATCH'] and not request.user.is_authenticated:
            return False
        if request.method == 'DELETE' and not request.user.is_staff:
            return False
        return True