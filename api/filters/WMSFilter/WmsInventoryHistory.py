import django_filters
from WMS.models.inventory import WmsInventoryHistory


class WmsInventoryHistoryFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''
    create_time_start = django_filters.DateTimeFilter('create_time', lookup_expr='gte')
    create_time_end = django_filters.DateTimeFilter('create_time', lookup_expr='lte')

    class Meta:
        model = WmsInventoryHistory
        # 精确过滤字段
        fields = {
            'creator__id': ['exact'],
            'editor__id': ['exact'],
            'inventory_movement__id': ['exact'],
            'inventory_movement__number': ['exact'],
            'inventory_receipt_order__id': ['exact'],
            'inventory_receipt_order__number': ['exact'],
            'inventory_shipment_order__id': ['exact'],
            'inventory_shipment_order__number': ['exact'],
            'inventory_shipment_order__to_user__id': ['exact'],
            'form_type': ['exact'],
            'number_type': ['icontains'],
            'item__id': ['exact'],
            'rack__id': ['exact'],
            'rack__warehouse__id': ['exact'],
            'rack__area__id': ['exact'],
            'remark': ['icontains']
        }
        # fields = '__all__'
