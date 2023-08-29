import django_filters
from WMS.models.warehouse import WmsRack


class WmsRackFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = WmsRack
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'number': ['icontains'], 'name': ['icontains'], 'area__id': ['exact'], 'remark': ['icontains']}
        # fields = '__all__'
