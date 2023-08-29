from WMS.models.movement import WmsInventoryMovementDetail
from rest_framework import permissions
from api.views.base import BulkModelViewSet
from api.serializers.WMSSerializer.WmsInventoryMovementDetail import WmsInventoryMovementDetailSerializer
from api.filters.WMSFilter.WmsInventoryMovementDetail import WmsInventoryMovementDetailFilter


class WmsInventoryMovementDetailViewSet(BulkModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsInventoryMovementDetail.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related('inventory_movement', 'inventory',
                                         'source_rack', 'source_rack__area', 'source_rack__area__warehouse',
                                         'target_rack', 'target_rack__area', 'target_rack__area__warehouse',
                                         'inventory__item', 'inventory__item__abs_item',
                                         'inventory__rack', 'inventory__rack__area', 'inventory__rack__area__warehouse')
    serializer_class = WmsInventoryMovementDetailSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsInventoryMovementDetailFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['remark']
