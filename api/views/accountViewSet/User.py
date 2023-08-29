from api.views.base import BaseViewSet
from account.models.user import User
from rest_framework.response import Response
from OpenWMS.permission import IsUserSelfCanEditAndAdminCanView
from rest_framework.permissions import IsAuthenticated
from api.serializers.accountSerializer.User import UserSerializer, MiniUserSerializer
from api.filters.accountFilter.User import UserFilter


class UserViewSet(BaseViewSet):
    '''
    用户信息 只允许查看自己的信息，不允许查看列表
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ('username', 'email', 'nickname', 'mobile', 'company__name', 'title', 'first_name')
    # 只允许用户自己查看自己的信息
    permission_classes = [IsUserSelfCanEditAndAdminCanView]
    filterset_class = UserFilter

    # 重载list 方法，仅管理员和可以查看自己的账户信息
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not request.user.is_superuser:
            queryset = queryset.filter(id=request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MiniUserViewSet(BaseViewSet):
    '''
    用户信息 只允许查看自己的信息，不允许查看列表
    '''
    queryset = User.objects.all()
    serializer_class = MiniUserSerializer
    search_fields = ('username', 'email', 'nickname', 'mobile', 'company__name', 'title', 'first_name')
    # 只允许用户自己查看自己的信息
    # permission_classes = [IsAuthenticated]
    filterset_class = UserFilter
