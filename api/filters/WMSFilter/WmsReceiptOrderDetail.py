import django_filters
from WMS.models.receipt import WmsReceiptOrderDetail
from api.filters.object_range import ObjectRangeQSFilterMixin


class WmsReceiptOrderDetailFilter(ObjectRangeQSFilterMixin, django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = WmsReceiptOrderDetail
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'receipt_order__id': ['exact'], 'item__id': ['exact'], 'rack__id': ['exact'],
                  'status': ['exact'], 'remark': ['icontains']}
        # fields = '__all__'
