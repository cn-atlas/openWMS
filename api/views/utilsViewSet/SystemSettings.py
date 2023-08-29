from api.views.base import BaseViewSet, ReadOnlyViewSet
from utils.models.system_info import SystemSettings
from rest_framework import permissions
from api.serializers.utilsSerializer.SystemSettings import SystemSettingsSerializer
from api.filters.utilsFilter.SystemSettings import SystemSettingsFilter


class SystemSettingsViewSet(ReadOnlyViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = SystemSettings.objects.all()
    queryset = queryset.prefetch_related()
    serializer_class = SystemSettingsSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = SystemSettingsFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['site_name', 'short_site_name', 'copy_right_company_name', 'system_name', 'record', 'record_link',
                     'version', 'other_info']
