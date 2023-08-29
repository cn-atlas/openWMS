from api.views.base import ReadOnlyViewSet
from WMS.models.inventory import WmsInventory
from rest_framework import permissions
from api.serializers.WMSSerializer.WmsInventory import WmsInventorySerializer
from api.filters.WMSFilter.WmsInventory import WmsInventoryFilter


class WmsInventoryViewSet(ReadOnlyViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsInventory.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related('item', 'item__abs_item', 'rack', 'rack__area__warehouse', 'rack__area')
    serializer_class = WmsInventorySerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsInventoryFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['remark', 'item__batch_number', 'item__remark', 'item__abs_item__number', 'item__abs_item__name',
                     'item__abs_item__model', 'item__abs_item__remark', 'item__abs_item__item_type__type_name']
