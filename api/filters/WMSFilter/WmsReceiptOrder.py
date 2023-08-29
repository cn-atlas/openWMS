import django_filters
from WMS.models.receipt import WmsReceiptOrder
from api.filters.object_range import ObjectRangeQSFilterMixin


class WmsReceiptOrderFilter(ObjectRangeQSFilterMixin, django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = WmsReceiptOrder
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'number': ['icontains'], 'receipt_type': ['exact'], 'supplier__id': ['exact'],
                  'order_no': ['icontains'], 'status': ['exact'], 'remark': ['icontains']}
        # fields = '__all__'
