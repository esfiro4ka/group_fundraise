from rest_framework.permissions import SAFE_METHODS, BasePermission


class CollectPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method in ['POST', 'PUT', 'DELETE']:
            return request.user and request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method in ['PUT', 'DELETE']:
            return obj.author == request.user
        return False
