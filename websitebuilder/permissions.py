from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'Admin' if request.user.role else False

class IsEditor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'Editor' if request.user.role else False

class IsViewer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'Viewer' if request.user.role else False

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role and request.user.role.name == 'Admin':
            return True
        return obj.owner == request.user