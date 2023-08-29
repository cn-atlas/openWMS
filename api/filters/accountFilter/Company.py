import django_filters
from account.models.department import Company


class CompanyFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = Company
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'number': ['icontains'], 'name': ['icontains'], 'person': ['icontains'], 'address': ['icontains'],
                  'phone': ['icontains'], 'note': ['icontains']}
        # fields = '__all__'
