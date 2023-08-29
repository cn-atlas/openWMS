from rest_framework import serializers
from api.serializers.base import BaseSerializer
from WMS.models.warehouse import WmsArea
from api.serializers.WMSSerializer.WmsWarehouse import WmsSimpleWarehouseSerializer


class WmsSimpleAreaSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    class Meta:
        model = WmsArea
        fields = ['id', 'number', 'name', 'warehouse', 'remark', 'url']


class WmsAreaSerializer(WmsSimpleAreaSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    warehouse_info = serializers.SerializerMethodField()

    def get_warehouse_info(self, instance):
        """ self referral field """
        serializer = WmsSimpleWarehouseSerializer(
            instance=instance.warehouse,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    class Meta:
        model = WmsArea
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'number', 'name', 'warehouse',
                  'warehouse_info', 'remark', 'url']
