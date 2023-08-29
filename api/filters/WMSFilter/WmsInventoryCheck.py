import django_filters
from WMS.models.check import WmsInventoryCheck
from api.filters.object_range import ObjectRangeQSFilterMixin


class WmsInventoryCheckFilter(ObjectRangeQSFilterMixin, django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = WmsInventoryCheck
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'is_checked': ['exact'], 'check_user__id': ['exact'], 'check_note': ['icontains'],
                  'number': ['icontains'], 'inventory_check_type': ['exact'],
                  'inventory_check_status': ['exact'], 'warehouse__id': ['exact'], 'area__id': ['exact'],
                  'rack__id': ['exact'], 'item__id': ['exact'], 'attachment__id': ['exact'], 'remark': ['icontains']}
        # fields = '__all__'
