import django_filters
from WMS.models.shipment import WmsDelivery
from api.filters.object_range import ObjectRangeQSFilterMixin


class WmsDeliveryFilter(ObjectRangeQSFilterMixin, django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = WmsDelivery
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'shipment_order__id': ['exact'], 'carrier': ['icontains'], 'tracking_no': ['icontains'],
                  'remark': ['icontains']}
        # fields = '__all__'
