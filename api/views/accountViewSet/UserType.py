from api.views.base import BaseViewSet
from account.models.user import UserType
from rest_framework import permissions
from api.serializers.accountSerializer.UserType import UserTypeSerializer
from api.filters.accountFilter.UserType import UserTypeFilter


class UserTypeViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = UserType.objects.all()
    queryset = queryset.prefetch_related()
    serializer_class = UserTypeSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = UserTypeFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['name', 'remark']
