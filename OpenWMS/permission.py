from rest_framework.permissions import BasePermission
from rest_framework import permissions


def read_only_permission(request, view):
    """
    先于 has_object_permission 调用, 只有 has_permission 为 True, 才会进一步验证 has_object_permission
    https://stackoverflow.com/questions/43064417/whats-the-differences-between-has-object-permission-and-has-permission-in-drfp#:~:text=has_permission%20is%20a%20check%20made,to%20check%20the%20ownership%20test.&text=This%20will%20also%20allow%20authenticated,new%20items%20or%20list%20them.
    has_object_permission 不支持 POST 方法
    Return `True` if permission is granted, `False` otherwise.
    """
    if request.method in permissions.SAFE_METHODS:
        return True


def admin_company_creator_has_permission(request, obj):
    """
    允许用户同单位同事或者管理员才能可以查看敏感信息
    """
    result = False
    if not request.user.is_anonymous:
        if request.user.is_superuser or request.user == obj.creator:
            result = True
        elif request.user.company == obj.creator.company and request.user.is_active and request.user.company:
            result = True
    return bool(result)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return read_only_permission(request, view)


class IsAuthenticatedCanCreateOwnerOrAdminCanEdit(BasePermission):
    """
    只要登录的用户就可以创建，但是只有创建者和管理员才可以看到该对象
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            return request.user.is_authenticated
        return admin_company_creator_has_permission(request, obj)


class IsUserSelfCanEditAndAdminCanView(BasePermission):
    """
    用户资料查看和修改权限, 仅支持管理员和用户本人查看, 仅支持用户本人修改
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return bool(request.user.is_superuser or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            return request.user == obj
        return bool(request.user.is_superuser or request.user == obj)
