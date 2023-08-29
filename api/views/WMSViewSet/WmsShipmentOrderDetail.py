from api.views.base import BulkModelViewSet
from WMS.models.shipment import WmsShipmentOrderDetail
from rest_framework import permissions
from api.serializers.WMSSerializer.WmsShipmentOrderDetail import WmsShipmentOrderDetailSerializer
from api.filters.WMSFilter.WmsShipmentOrderDetail import WmsShipmentOrderDetailFilter


class WmsShipmentOrderDetailViewSet(BulkModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsShipmentOrderDetail.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related('shipment_order',
                                         'rack', 'rack__area', 'rack__area__warehouse',
                                         'inventory',
                                         'inventory__item', 'inventory__item__abs_item',
                                         'inventory__rack', 'inventory__rack__area', 'inventory__rack__area__warehouse')
    serializer_class = WmsShipmentOrderDetailSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsShipmentOrderDetailFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['remark']
