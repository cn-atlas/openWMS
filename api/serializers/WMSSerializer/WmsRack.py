from rest_framework import serializers
from api.serializers.base import BaseSerializer
from api.serializers.WMSSerializer.WmsWarehouse import WmsSimpleWarehouseSerializer
from api.serializers.WMSSerializer.WmsArea import WmsAreaSerializer
from WMS.models.warehouse import WmsRack


class WmsSimpleRackSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    class Meta:
        model = WmsRack
        fields = ['id', 'number', 'name', 'remark', 'url']


class WmsRackSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    area_info = serializers.SerializerMethodField()

    def get_area_info(self, instance):
        """ self referral field """
        serializer = WmsAreaSerializer(
            instance=instance.area,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    class Meta:
        model = WmsRack
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'number', 'name',
                  'area', 'area_info', 'remark', 'url']
