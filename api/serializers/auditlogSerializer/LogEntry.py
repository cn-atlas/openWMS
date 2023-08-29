from rest_framework import serializers
from api.serializers.base import BaseSerializer
from auditlog.models import LogEntry


class LogEntrySerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''
     
    class Meta:
        model = LogEntry
        fields = ['id', 'content_type', 'object_pk', 'object_id', 'object_repr', 'serialized_data', 'action', 'changes', 'actor', 'remote_addr', 'timestamp', 'additional_data', 'url'] 
