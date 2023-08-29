from django_filters import rest_framework as filters
from WMS.models.shipment import WmsShipmentOrderDetail
from api.filters.object_range import ObjectRangeQSFilterMixin


class WmsShipmentOrderDetailFilter(ObjectRangeQSFilterMixin, filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = WmsShipmentOrderDetail
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'shipment_order__id': ['exact'], 'inventory__id': ['exact'], 'inventory__item__id': ['exact'],
                  'rack__id': ['exact'], 'status': ['exact'], 'remark': ['icontains']}
        # fields = '__all__'
