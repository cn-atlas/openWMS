from rest_framework import serializers
from api.serializers.base import BaseSerializer
from utils.models.attachment import InventoryFile


class InventoryFileSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''
     
    class Meta:
        model = InventoryFile
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'name', 'uuid', 'type', 'remark', 'file', 'url'] 
