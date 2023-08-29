from api.views.base import BaseViewSet
from account.models.department import Department
from rest_framework import permissions
from api.serializers.accountSerializer.Department import DepartmentSerializer
from api.filters.accountFilter.Department import DepartmentFilter


class DepartmentViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Department.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related()
    serializer_class = DepartmentSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = DepartmentFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['department_number', 'department_name', 'remark']
