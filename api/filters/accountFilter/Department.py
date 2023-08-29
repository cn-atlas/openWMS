import django_filters
from account.models.department import Department


class DepartmentFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = Department
        # 精确过滤字段
        fields = {'id': ['exact'], 'is_show': ['exact'], 'creator__id': ['exact'], 'editor__id': ['exact'],
                  'parent__id': ['exact'], 'company__id': ['exact'], 'department_number': ['icontains'],
                  'department_name': ['icontains'], 'remark': ['icontains'], 'lft': ['exact'], 'rght': ['exact'],
                  'tree_id': ['exact'], 'level': ['exact']}
        # fields = '__all__'
