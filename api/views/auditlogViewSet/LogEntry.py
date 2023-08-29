from api.views.base import BaseViewSet
from auditlog.models import LogEntry
from rest_framework import permissions
from api.serializers.auditlogSerializer.LogEntry import LogEntrySerializer
from api.filters.auditlogFilter.LogEntry import LogEntryFilter


class LogEntryViewSet(BaseViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = LogEntry.objects.all()
    queryset = queryset.prefetch_related()
    serializer_class = LogEntrySerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = LogEntryFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['object_pk', 'object_repr', 'changes']
