from api.views.base import BaseViewSet
from WMS.models.warehouse import WmsRack
from rest_framework import permissions
from api.serializers.WMSSerializer.WmsRack import WmsRackSerializer
from api.filters.WMSFilter.WmsRack import WmsRackFilter


class WmsRackViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = WmsRack.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related('area', 'area__warehouse')
    serializer_class = WmsRackSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = WmsRackFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['number', 'name', 'remark']
