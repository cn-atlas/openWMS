from django_filters import rest_framework as filters
from account.models.ui_router import UIRouter


class UIRouterFilter(filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = UIRouter
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'parent__id': ['exact'], 'name': ['icontains'], 'code': ['icontains'], 'path': ['icontains'],
                  'icon': ['icontains'], 'component': ['icontains'], 'redirect': ['icontains'], 'target': ['icontains'],
                  'hide_in_menu': ['exact'], 'hide_children_in_menu': ['exact'], 'hide_breadcrumb': ['exact'],
                  'priority': ['exact'], 'remark': ['icontains'], 'lft': ['exact'], 'rght': ['exact'],
                  'tree_id': ['exact'], 'level': ['exact']}
        # fields = '__all__'
