import django_filters
from account.models.user import ValidCode


class ValidCodeFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = ValidCode
        # 精确过滤字段
        fields = {'id': ['exact'], 'credential': ['icontains'], 'valid_type': ['icontains'],
                  'valid_code': ['icontains'], 'uuid': ['icontains']}
        # fields = '__all__'
