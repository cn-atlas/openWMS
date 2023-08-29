import django_filters
from utils.models.system_info import SystemSettings


class SystemSettingsFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = SystemSettings
        # 精确过滤字段
        fields = {'id': ['exact'], 'site_name': ['icontains'], 'short_site_name': ['icontains'],
                  'copy_right_company_name': ['icontains'], 'system_name': ['icontains'], 'record': ['icontains'],
                  'record_link': ['icontains'], 'version': ['icontains'], 'other_info': ['icontains'],
                  'small_logo__id': ['exact'], 'big_logo__id': ['exact'], 'other_icon__id': ['exact']}
        # fields = '__all__'
