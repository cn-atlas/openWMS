import django_filters
from WMS.models.receipt import WmsSupplier


class WmsSupplierFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = WmsSupplier
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'number': ['icontains'], 'name': ['icontains'], 'bank_name': ['icontains'],
                  'bank_account': ['icontains'], 'address': ['icontains'], 'mobile_no': ['icontains'],
                  'tel_no': ['icontains'], 'contact': ['icontains'], 'level': ['icontains'], 'email': ['icontains'],
                  'remark': ['icontains']}
        # fields = '__all__'
