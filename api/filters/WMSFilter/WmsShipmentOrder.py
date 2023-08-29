import django_filters
from WMS.models.shipment import WmsShipmentOrder
from api.filters.object_range import ObjectRangeQSFilterMixin


class WmsShipmentOrderFilter(ObjectRangeQSFilterMixin, django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = WmsShipmentOrder
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'is_checked': ['exact'], 'check_user__id': ['exact'], 'check_note': ['icontains'],
                  'number': ['icontains'], 'shipment_order_type': ['exact'], 'order_no': ['icontains'],
                  'to_customer': ['icontains'], 'to_user__id': ['exact'], 'status': ['exact'],
                  'remark': ['icontains']}
        # fields = '__all__'
