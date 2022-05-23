from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = 'Вносить изменения может только автор рецепта!'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            (request.method in permissions.SAFE_METHODS
             or obj.author == request.user)
        )


class IsUserOrReadonly(permissions.BasePermission):
    message = 'Только сам пользователь может изменять свои данные!'

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            (request.method in permissions.SAFE_METHODS
             or obj.pk == user.pk)
        )
