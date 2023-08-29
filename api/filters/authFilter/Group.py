import django_filters
from django.contrib.auth.models import Group


class GroupFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = Group
        # 精确过滤字段
        fields = {'id': ['exact'], 'name': ['icontains']}
        # fields = '__all__'
