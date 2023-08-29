from api.views.base import BaseViewSet
from WMS.models.receipt import WmsSupplier
from rest_framework import permissions
from api.serializers.WMSSerializer.WmsSupplier import WmsSupplierSerializer
from api.filters.WMSFilter.WmsSupplier import WmsSupplierFilter


class WmsSupplierViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsSupplier.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related()
    serializer_class = WmsSupplierSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsSupplierFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['number', 'name', 'bank_name', 'bank_account', 'address', 'mobile_no', 'tel_no', 'contact',
                     'level', 'email', 'remark']
