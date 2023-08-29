import django_filters
from utils.models.attachment import CommonFile
from api.filters.object_range import ObjectRangeQSFilterMixin


class CommonFileFilter(ObjectRangeQSFilterMixin, django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = CommonFile
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'name': ['icontains'], 'uuid': ['icontains'], 'type': ['icontains'], 'remark': ['icontains']}
        # fields = '__all__'
