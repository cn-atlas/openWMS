import django_filters
from WMS.models.check import WmsInventoryCheckDetail
from api.filters.object_range import ObjectRangeQSFilterMixin


class WmsInventoryCheckDetailFilter(ObjectRangeQSFilterMixin, django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = WmsInventoryCheckDetail
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'inventory_check__id': ['exact'], 'rack__id': ['exact'], 'item__id': ['exact'],
                  'remark': ['icontains']}
        # fields = '__all__'
