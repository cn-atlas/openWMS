from rest_framework import serializers
from api.serializers.base import BaseSerializer
from account.models.department import Company


class CompanySerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''
     
    class Meta:
        model = Company
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'number', 'name', 'person', 'address', 'phone', 'note', 'url'] 
