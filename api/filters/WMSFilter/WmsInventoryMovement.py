import django_filters
from WMS.models.movement import WmsInventoryMovement
from api.filters.object_range import ObjectRangeQSFilterMixin


class WmsInventoryMovementFilter(ObjectRangeQSFilterMixin, django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = WmsInventoryMovement
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'is_checked': ['exact'], 'check_user__id': ['exact'], 'check_note': ['icontains'],
                  'number': ['icontains'], 'source_rack__id': ['exact'], 'target_rack__id': ['exact'],
                  'status': ['exact'], 'remark': ['icontains']}
        # fields = '__all__'
