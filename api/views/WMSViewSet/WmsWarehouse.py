from api.views.base import BaseViewSet
from WMS.models.warehouse import WmsWarehouse
from rest_framework import permissions
from api.serializers.WMSSerializer.WmsWarehouse import WmsWarehouseSerializer
from api.filters.WMSFilter.WmsWarehouse import WmsWarehouseFilter


class WmsWarehouseViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsWarehouse.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related()
    serializer_class = WmsWarehouseSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsWarehouseFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['number', 'name', 'remark']
