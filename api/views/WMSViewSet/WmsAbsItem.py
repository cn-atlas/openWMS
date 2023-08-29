from api.views.base import BaseViewSet
from WMS.models.item import WmsAbsItem
from rest_framework import permissions
from api.serializers.WMSSerializer.WmsAbsItem import WmsAbsItemSerializer
from api.filters.WMSFilter.WmsAbsItem import WmsAbsItemFilter


class WmsAbsItemViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsAbsItem.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related('item_type')
    serializer_class = WmsAbsItemSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsAbsItemFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['number', 'name', 'specs', 'model', 'unit', 'remark']
