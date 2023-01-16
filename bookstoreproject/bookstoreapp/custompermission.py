from rest_framework import permissions


class IsCurrentUserOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner == request.user

    def has_view_permission(self, request, obj):
        if request.user.is_superuser:
            return True
        elif request.user == obj.owner:
            return True
        else:
            return False

    def has_update_permission(self, request, obj):
        if request.user.is_superuser:
            return True
        elif request.user == obj.owner:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj):
        if request.user.is_superuser:
            return True
        elif request.user == obj.owner:
            return True
        else:
            return False

