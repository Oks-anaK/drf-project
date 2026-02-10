from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором.
    """

    message = "Вы модератор"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем.
    """

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsUserOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем своего профиля.
    """

    def has_object_permission(self, request, view, obj):
        # Проверяем, что объект - это профиль текущего пользователя
        return obj == request.user
