from api.views.base import BaseViewSet
from utils.models.attachment import InventoryFile
from rest_framework import permissions
from api.serializers.utilsSerializer.InventoryFile import InventoryFileSerializer
from api.filters.utilsFilter.InventoryFile import InventoryFileFilter


class InventoryFileViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = InventoryFile.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related()
    serializer_class = InventoryFileSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = InventoryFileFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['name', 'uuid', 'type', 'remark']
