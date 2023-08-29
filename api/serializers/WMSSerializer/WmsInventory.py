from rest_framework import serializers
from api.serializers.base import BaseSerializer
from api.serializers.WMSSerializer import WmsItemSerializer
from api.serializers.WMSSerializer.WmsRack import WmsRackSerializer
from WMS.models.inventory import WmsInventory


class WmsInventorySerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    库存只读，都是根据单据生成不允许更改
    '''

    item_info = serializers.SerializerMethodField()
    rack_info = serializers.SerializerMethodField()

    def get_item_info(self, instance):
        """ self referral field """
        serializer = WmsItemSerializer(
            instance=instance.item,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    def get_rack_info(self, instance):
        """ self referral field """
        serializer = WmsRackSerializer(
            instance=instance.rack,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    class Meta:
        model = WmsInventory
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'rack', 'rack_info', 'item',
                  'item_info', 'quantity', 'remark', 'url']
