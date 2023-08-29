from api.views.base import BaseViewSet
from WMS.models.shipment import WmsShipmentOrder
from rest_framework import permissions
from api.serializers.WMSSerializer.WmsShipmentOrder import WmsShipmentOrderSerializer
from api.filters.WMSFilter.WmsShipmentOrder import WmsShipmentOrderFilter


class WmsShipmentOrderViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsShipmentOrder.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related('to_user')
    serializer_class = WmsShipmentOrderSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsShipmentOrderFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['check_note', 'number', 'order_no', 'to_customer', 'remark']
