from api.views.base import BaseViewSet
from WMS.models.item import WmsItemType
from rest_framework import permissions
from api.serializers.WMSSerializer.WmsItemType import WmsItemTypeSerializer
from api.filters.WMSFilter.WmsItemType import WmsItemTypeFilter


class WmsItemTypeViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsItemType.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related()
    serializer_class = WmsItemTypeSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsItemTypeFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['type_name', 'status']
