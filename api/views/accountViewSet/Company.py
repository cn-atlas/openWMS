from api.views.base import BaseViewSet
from account.models.department import Company
from rest_framework import permissions
from api.serializers.accountSerializer.Company import CompanySerializer
from api.filters.accountFilter.Company import CompanyFilter


class CompanyViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Company.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related()
    serializer_class = CompanySerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = CompanyFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['number', 'name', 'person', 'address', 'phone', 'note']
