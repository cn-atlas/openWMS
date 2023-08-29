from api.views.base import BaseViewSet
from account.models.user import ValidCode
from rest_framework import permissions
from api.serializers.accountSerializer.ValidCode import ValidCodeSerializer
from api.filters.accountFilter.ValidCode import ValidCodeFilter


class ValidCodeViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = ValidCode.objects.all()
    queryset = queryset.prefetch_related()
    serializer_class = ValidCodeSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = ValidCodeFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['credential', 'valid_type', 'valid_code', 'uuid']
