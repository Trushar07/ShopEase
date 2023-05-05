from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


"""
More about Permissions

1. DjangoModelPermissions allows us to set any combination of permissions to each of the 
users separately. The permission then checks if the user is authenticated and if they have add , change , 
or delete user permissions on the model.

2. DjangoModelPermissionsOrAnonReadOnly
Similar to DjangoModelPermissions, but also allows unauthenticated users to have read-only access to the API.
"""
