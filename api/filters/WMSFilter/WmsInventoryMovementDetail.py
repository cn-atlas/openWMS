from django_filters import rest_framework as filters
from WMS.models.movement import WmsInventoryMovementDetail
from api.filters.object_range import ObjectRangeQSFilterMixin


class WmsInventoryMovementDetailFilter(ObjectRangeQSFilterMixin, filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = WmsInventoryMovementDetail
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'inventory_movement__id': ['exact'], 'inventory__id': ['exact'], 'inventory__item__id': ['exact'],
                  'source_rack__id': ['exact'], 'target_rack__id': ['exact'], 'status': ['exact'],
                  'remark': ['icontains']}
        # fields = '__all__'
