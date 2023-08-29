from rest_framework.permissions import BasePermission


class CanExport(BasePermission):
    """
    能不能导出数据 根据 Django model 的 view 权限初步确定，更详细的权限依靠 object_range 决定
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if hasattr(view, 'Meta') and hasattr(view.Meta, 'model'):
            model_name = view.Meta.model.__name__
            app_name = view.Meta.model._meta.app_label
            permission_codename = app_name + ".view_" + model_name.lower()
            # Check if the user has the permission
            if request.user.has_perm(permission_codename):
                return True
        return False
