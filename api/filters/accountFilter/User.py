import django_filters
from account.models.user import User


class UserFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = User
        # 精确过滤字段
        fields = {'id': ['exact'], 'password': ['icontains'], 'is_superuser': ['exact'], 'username': ['icontains'],
                  'first_name': ['icontains'], 'last_name': ['icontains'], 'is_staff': ['exact'],
                  'is_active': ['exact'], 'user_code': ['icontains'], 'title': ['icontains'], 'email': ['icontains'],
                  'nickname': ['icontains'], 'mobile': ['icontains'], 'description': ['icontains'],
                  'cls__id': ['exact'], 'gender': ['icontains'], 'company__id': ['exact'], 'department__id': ['exact'],
                  'is_director': ['exact'], 'position': ['icontains'], 'job_number': ['icontains'],
                  'icon__id': ['exact']}
        # fields = '__all__'
