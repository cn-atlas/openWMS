from WMS.models.check import WmsInventoryCheckDetail
from rest_framework import permissions
from api.views.base import BulkModelViewSet
from api.serializers.WMSSerializer.WmsInventoryCheckDetail import WmsInventoryCheckDetailSerializer
from api.filters.WMSFilter.WmsInventoryCheckDetail import WmsInventoryCheckDetailFilter


class WmsInventoryCheckDetailViewSet(BulkModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsInventoryCheckDetail.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related('inventory_check', 'item', 'item__abs_item', 'rack')
    serializer_class = WmsInventoryCheckDetailSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsInventoryCheckDetailFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['remark']
