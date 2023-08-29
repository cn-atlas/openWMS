import django_filters
from WMS.models.item import WmsItemType


class WmsItemTypeFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = WmsItemType
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'parent__id': ['exact'], 'type_name': ['icontains'], 'status': ['icontains'], 'lft': ['exact'],
                  'rght': ['exact'], 'tree_id': ['exact'], 'level': ['exact']}
        # fields = '__all__'
