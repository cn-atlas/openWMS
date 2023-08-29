from api.views.base import BaseViewSet
from WMS.models.warehouse import WmsArea
from rest_framework import permissions
from api.serializers.WMSSerializer.WmsArea import WmsAreaSerializer
from api.filters.WMSFilter.WmsArea import WmsAreaFilter


class WmsAreaViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsArea.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related('warehouse')
    serializer_class = WmsAreaSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsAreaFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['number', 'name', 'remark']
