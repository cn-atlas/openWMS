import django_filters
from account.models.user import UserType


class UserTypeFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = UserType
        # 精确过滤字段
        fields = {'id': ['exact'], 'name': ['icontains'], 'remark': ['icontains']}
        # fields = '__all__'
