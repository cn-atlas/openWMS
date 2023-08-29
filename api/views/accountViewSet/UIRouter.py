from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from api.views.base import BaseViewSet, BaseAPIViewSet
from account.models.ui_router import UIRouter
from rest_framework import permissions
from api.serializers.accountSerializer.UIRouter import UIRouterSerializer, UIRouterListSerializer
from api.filters.accountFilter.UIRouter import UIRouterFilter


class UIRouterViewSet(BaseViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = UIRouter.objects.filter(is_show=True).order_by("-priority").all()
    # queryset = queryset.prefetch_related('son_uirouter', 'x_authority', 'creator', 'editor')
    serializer_class = UIRouterSerializer
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filter_class = UIRouterFilter

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = ['name', 'code', 'path', 'component', 'redirect', 'target', 'remark']


class GetRouterViewSet(GenericAPIView):
    """
    # https://www.py4u.net/discuss/1260893
    或许也可以尝试一下这么用 from https://stackoverflow.com/a/5740724：
    from django.db.models import Q
    import operator
    from functools import reduce


    def get_queryset_descendants(nodes, include_self=False):
        if not nodes:
            return UIRouter.objects.none()
        filters = []
        for n in nodes:
            lft, rght = n.lft, n.rght
            if include_self:
                lft -= 1
                rght += 1
            filters.append(Q(tree_id=n.tree_id, lft__gt=lft, rght__lt=rght))
        q = reduce(operator.or_, filters)
        return UIRouter.objects.filter(q)
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UIRouterListSerializer

    def get(self, request, *args, **kwargs):
        # prefetch_related 优化菜单加载速度, 不能排序 .order_by("-priority")
        root_nodes = UIRouter.objects.filter(is_show=True).all().prefetch_related("x_authority").get_cached_trees()
        ordered_root_nodes = list(root_nodes)
        ordered_root_nodes.sort(key=lambda x: x.priority, reverse=True)
        data = []
        for n in ordered_root_nodes:
            data.append(self.recursive_node_to_dict(n))
        return Response(data)

    def recursive_node_to_dict(self, node):
        result = self.get_serializer(instance=node).data
        children = [self.recursive_node_to_dict(c) for c in node.get_children()]
        if children:
            result["routes"] = children
        return result
