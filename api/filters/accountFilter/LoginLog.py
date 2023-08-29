import django_filters
from account.models.user import LoginLog


class LoginLogFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = LoginLog
        # 精确过滤字段
        fields = {'id': ['exact'], 'credential': ['icontains'], 'method': ['icontains'],
                  'login_username': ['icontains'], 'ip': ['icontains'], 'city': ['icontains'], 'agent': ['icontains'],
                  'remark': ['icontains'], 'status': ['exact']}
        # fields = '__all__'
