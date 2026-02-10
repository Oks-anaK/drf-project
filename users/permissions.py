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
    Пользователь может редактировать/удалять только свой профиль.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user or obj.id == request.user.id


class IsNotModeratorAndOwner(permissions.BasePermission):
    """
    Проверяет, что пользователь НЕ модератор И является владельцем объекта.
    Используется для удаления: модераторы не могут удалять, только владельцы могут.
    """

    def has_permission(self, request, view):
        # Пользователь не модератор
        return not request.user.groups.filter(name="moderators").exists()

    def has_object_permission(self, request, view, obj):
        # Пользователь является владельцем
        return obj.owner == request.user