from api.views.base import BaseViewSet
from WMS.models.shipment import WmsDelivery
from rest_framework import permissions
from api.serializers.WMSSerializer.WmsDelivery import WmsDeliverySerializer
from api.filters.WMSFilter.WmsDelivery import WmsDeliveryFilter


class WmsDeliveryViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsDelivery.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related('shipment_order')
    serializer_class = WmsDeliverySerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsDeliveryFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['carrier', 'tracking_no', 'remark']
