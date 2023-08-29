import django_filters
from WMS.models.item import WmsAbsItem


class WmsAbsItemFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = WmsAbsItem
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'number': ['icontains'], 'name': ['icontains'], 'specs': ['icontains'], 'model': ['icontains'],
                  'item_type__id': ['exact'], 'unit': ['icontains'], 'remark': ['icontains']}
        # fields = '__all__'
