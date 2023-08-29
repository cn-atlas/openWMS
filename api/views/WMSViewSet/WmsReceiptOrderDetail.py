from api.views.base import BulkModelViewSet
from WMS.models.receipt import WmsReceiptOrderDetail
from rest_framework import permissions
from api.serializers.WMSSerializer.WmsReceiptOrderDetail import WmsReceiptOrderDetailSerializer
from api.filters.WMSFilter.WmsReceiptOrderDetail import WmsReceiptOrderDetailFilter


class WmsReceiptOrderDetailViewSet(BulkModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsReceiptOrderDetail.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related('receipt_order', 'item', 'item__abs_item', 'rack', 'rack__area',
                                         'rack__area__warehouse')
    serializer_class = WmsReceiptOrderDetailSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsReceiptOrderDetailFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['remark']
