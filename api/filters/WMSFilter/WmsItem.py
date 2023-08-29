import django_filters
from WMS.models.item import WmsItem


class WmsItemFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = WmsItem
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'abs_item__id': ['exact'], 'abs_item__number': ['exact'], 'abs_item__name': ['icontains'],
                  'batch_number': ['icontains'], 'remark': ['icontains']}
        # fields = '__all__'
