import django_filters
from auditlog.models import LogEntry


class LogEntryFilter(django_filters.FilterSet):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = LogEntry
        # 精确过滤字段
        fields = {'id': ['exact'], 'content_type__id': ['exact'], 'object_pk': ['icontains'], 'object_id': ['exact'],
                  'object_repr': ['icontains'], 'action': ['exact'], 'changes': ['icontains'], 'actor__id': ['exact']}
        # fields = '__all__'
