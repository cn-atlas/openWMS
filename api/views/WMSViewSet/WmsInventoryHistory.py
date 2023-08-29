from api.views.base import ReadOnlyViewSet
from WMS.models.inventory import WmsInventoryHistory
from rest_framework import permissions
from api.serializers.WMSSerializer.WmsInventoryHistory import WmsInventoryHistorySerializer
from api.filters.WMSFilter.WmsInventoryHistory import WmsInventoryHistoryFilter


class WmsInventoryHistoryViewSet(ReadOnlyViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsInventoryHistory.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related('item', 'item__abs_item', 'rack', 'rack__area', 'rack__area__warehouse',
                                         'inventory_movement', 'inventory_receipt_order', 'inventory_shipment_order')
    serializer_class = WmsInventoryHistorySerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsInventoryHistoryFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['number_type', 'remark']
