from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework_bulk import mixins as bulk_mixins


def _get_queryset(cls, queryset):
    # 从GET参数中获取ordering参数，默认为空
    ordering = cls.request.query_params.get('ordering', None)
    if ordering:
        # 如果有ordering参数，则使用order_by方法来排序
        queryset = queryset.order_by(ordering)
    else:
        queryset = queryset.order_by('-pk')
    return queryset


class NoDeleteViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      # mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """
    禁止api接口删除所有数据
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        return _get_queryset(self, queryset)


class WithDeleteViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    """
    允许api接口删除数据
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        return _get_queryset(self, queryset)


class BaseViewSet(NoDeleteViewSet):
    '''
    所有需要记录编辑人信息的基类，允许用户查看霍编辑API路径
    '''
    # search_fields = "__all__"
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)

    # http_method_names = [m for m in super().http_method_names if m != 'delete']


class WithDeleteBaseViewSet(WithDeleteViewSet):
    '''
    所有需要记录编辑人信息的基类，允许用户查看霍编辑API路径
    '''
    # search_fields = "__all__"
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
    # http_method_names = [m for m in super().http_method_names if m != 'delete']


class BaseAPIViewSet(APIView):
    '''
    所有使用APIView的视图都继承此基类
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response_data = {
            'success': False,
            'code': None,
            'msg': None,
            'data': None
        }


# ########################################################## #
# Concrete viewset classes that provide method handlers      #
# by composing the bulk mixin classes with the base viewset. #
# ########################################################## #

class BulkModelViewSet(bulk_mixins.BulkCreateModelMixin,
                       bulk_mixins.BulkUpdateModelMixin,
                       # bulk_mixins.BulkDestroyModelMixin,
                       BaseViewSet):
    pass


class ReadOnlyViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    """
    只读数据接口
    """

    def get_queryset(self):
        queryset = super().get_queryset()
        return _get_queryset(self, queryset)
