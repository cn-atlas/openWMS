from api.views.base import BaseViewSet
from WMS.models.item import WmsItem
from rest_framework import permissions
from api.serializers.WMSSerializer.WmsItem import WmsItemSerializer
from api.filters.WMSFilter.WmsItem import WmsItemFilter


class WmsItemViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsItem.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related('abs_item')
    serializer_class = WmsItemSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsItemFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['batch_number', 'remark']
