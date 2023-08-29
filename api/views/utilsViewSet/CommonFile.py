from api.views.base import BaseViewSet
from utils.models.attachment import CommonFile
from rest_framework import permissions
from api.serializers.utilsSerializer.CommonFile import CommonFileSerializer
from api.filters.utilsFilter.CommonFile import CommonFileFilter


class CommonFileViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = CommonFile.objects.filter(is_show=True).all()
    queryset = queryset.prefetch_related()
    serializer_class = CommonFileSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = CommonFileFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['name', 'uuid', 'type', 'remark']
