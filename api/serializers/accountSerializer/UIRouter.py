from rest_framework import serializers
from api.serializers.base import BaseSerializer
from account.models.ui_router import UIRouter


class UIRouterSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    class Meta:
        model = UIRouter
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'parent', 'name', 'code', 'path',
                  'icon', 'component', 'redirect', 'target', 'hide_in_menu', 'hide_children_in_menu', 'hide_breadcrumb',
                  'remark', 'url']


class UIRouterListSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    # https://www.py4u.net/discuss/1260893
    '''

    permissions = serializers.SerializerMethodField()
    access = serializers.SerializerMethodField()

    def get_permissions(self, instance):
        authority_names = []
        authorities = instance.x_authority.all()
        if authorities:
            for authority in authorities:
                authority_names.append(authority.codename)
        return authority_names

    def get_access(self, instance):
        """
        前端指定要的 @沈阳

        :param instance:
        :return:
        """
        return "normalRouteFilter"

    class Meta:
        model = UIRouter
        fields = ['name', 'code', 'path', 'access', 'permissions',
                  'icon', 'component', 'redirect', 'target', 'hide_in_menu', 'hide_children_in_menu', 'hide_breadcrumb']
