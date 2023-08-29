from django.db.models import Q
from django.http.response import JsonResponse
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import Permission


def get_user_permissions_queryset(user):
    if user.is_superuser:
        return Permission.objects
    return user.user_permissions.all() | Permission.objects.filter(
        Q(group__depart_groups__department_users=user) | Q(group__user=user) | Q(group__name__icontains="公共权限"))


def get_user_permission_code_names(user):
    code_name_set_list = get_user_permissions_queryset(user).all().values_list("codename")
    code_names = list()
    for code_name_set in code_name_set_list:
        code_names.extend(list(code_name_set))
    code_names = list(set(code_names))
    return code_names


class GetUserPermissionViewSet(GenericAPIView):
    """
    获取当前用户权限
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        data = get_user_permission_code_names(request.user)
        return JsonResponse(data, safe=False)
