from api.views.base import BaseViewSet
from WMS.models.movement import WmsInventoryMovement
from rest_framework import permissions
from api.serializers.WMSSerializer.WmsInventoryMovement import WmsInventoryMovementSerializer
from api.filters.WMSFilter.WmsInventoryMovement import WmsInventoryMovementFilter


class WmsInventoryMovementViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsInventoryMovement.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related('source_rack', 'target_rack', 'source_rack__area',
                                         'source_rack__area__warehouse', 'target_rack__area',
                                         'target_rack__area__warehouse')
    serializer_class = WmsInventoryMovementSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsInventoryMovementFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['check_note', 'number', 'remark']
