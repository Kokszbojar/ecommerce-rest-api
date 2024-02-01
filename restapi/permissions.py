from rest_framework import permissions


class IsOwnerOrAdminOnly(permissions.BasePermission):
    '''
    Custom permission to only allow owners of an object
    or administrators to edit it.
    '''

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        else:
            return obj.client == request.user
