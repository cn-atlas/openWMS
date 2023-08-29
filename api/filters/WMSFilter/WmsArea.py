import django_filters
from WMS.models.warehouse import WmsArea


class WmsAreaFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = WmsArea
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'number': ['icontains'], 'name': ['icontains'], 'warehouse__id': ['exact'], 'remark': ['icontains']}
        # fields = '__all__'
