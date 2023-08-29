from rest_framework import serializers
from api.serializers.base import BaseSerializer
from account.models.user import ValidCode


class ValidCodeSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''
     
    class Meta:
        model = ValidCode
        fields = ['id', 'credential', 'valid_type', 'valid_code', 'uuid', 'create_time', 'modify_time', 'url'] 
