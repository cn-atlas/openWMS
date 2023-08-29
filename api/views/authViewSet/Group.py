from api.views.base import BaseViewSet
from django.contrib.auth.models import Group
from rest_framework import permissions
from api.serializers.authSerializer.Group import GroupSerializer
from api.filters.authFilter.Group import GroupFilter


class GroupViewSet(BaseViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Group.objects.all()
    queryset = queryset.prefetch_related()
    serializer_class = GroupSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = GroupFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['name']
