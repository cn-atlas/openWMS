from api.views.base import BaseViewSet
from WMS.models.receipt import WmsReceiptOrder
from rest_framework import permissions
from api.serializers.WMSSerializer.WmsReceiptOrder import WmsReceiptOrderSerializer
from api.filters.WMSFilter.WmsReceiptOrder import WmsReceiptOrderFilter


class WmsReceiptOrderViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsReceiptOrder.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related()
    serializer_class = WmsReceiptOrderSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsReceiptOrderFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['number', 'order_no', 'remark']
