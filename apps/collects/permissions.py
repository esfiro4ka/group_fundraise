from rest_framework.permissions import SAFE_METHODS, BasePermission


class CollectPermission(BasePermission):
    """
    Права доступа для групповых денежных сборов.

    Разрешает GET запросы всем пользователям.
    Разрешает POST, PUT и DELETE запросы аутентифицированным пользователям.

    При проверке объектных разрешений:
    - Разрешает SAFE_METHODS (GET, HEAD, OPTIONS) всем пользователям.
    - Разрешает PUT и DELETE запросы только автору объекта.
    """

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
