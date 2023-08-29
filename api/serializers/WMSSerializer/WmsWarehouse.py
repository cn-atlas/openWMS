from rest_framework import serializers
from api.serializers.base import BaseSerializer
from WMS.models.warehouse import WmsWarehouse


class WmsSimpleWarehouseSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    class Meta:
        model = WmsWarehouse
        fields = ['id', 'number', 'name', 'remark', 'url']


class WmsWarehouseSerializer(WmsSimpleWarehouseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    class Meta:
        model = WmsWarehouse
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'number', 'name', 'remark', 'url']
