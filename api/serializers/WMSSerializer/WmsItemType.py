from rest_framework import serializers
from api.serializers.base import BaseSerializer
from WMS.models.item import WmsItemType


class WmsSimpleItemTypeSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    class Meta:
        model = WmsItemType
        fields = ['id', 'type_name', 'url']


class WmsItemTypeSerializer(WmsSimpleItemTypeSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    class Meta:
        model = WmsItemType
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'parent', 'type_name', 'status',
                  'lft', 'rght', 'tree_id', 'level', 'url']
