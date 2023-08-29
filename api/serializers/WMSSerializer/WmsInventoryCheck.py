from rest_framework import serializers
from api.validators.check import validate_non
from api.serializers.base import BaseSerializer
from WMS.models.check import WmsInventoryCheck
from api.serializers.WMSSerializer import WmsItemSerializer
from api.serializers.utilsSerializer import InventoryFileSerializer
from api.serializers.WMSSerializer.WmsWarehouse import WmsSimpleWarehouseSerializer
from api.serializers.WMSSerializer.WmsArea import WmsSimpleAreaSerializer
from api.serializers.WMSSerializer.WmsRack import WmsSimpleRackSerializer


class WmsSimpleInventoryCheckSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    def validate(self, attrs):
        return validate_non(self, attrs)

    class Meta:
        model = WmsInventoryCheck
        fields = ['id', 'is_checked', 'number', 'inventory_check_type', 'inventory_check_status',
                  'inventory_check_total', 'remark', 'url']


class WmsInventoryCheckSerializer(WmsSimpleInventoryCheckSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    warehouse_info = serializers.SerializerMethodField()
    area_info = serializers.SerializerMethodField()
    rack_info = serializers.SerializerMethodField()
    item_info = serializers.SerializerMethodField()
    attachment_info = serializers.SerializerMethodField()

    def get_warehouse_info(self, instance):
        """ self referral field """
        serializer = WmsSimpleWarehouseSerializer(
            instance=instance.warehouse,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    def get_area_info(self, instance):
        """ self referral field """
        serializer = WmsSimpleAreaSerializer(
            instance=instance.area,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    def get_rack_info(self, instance):
        """ self referral field """
        serializer = WmsSimpleRackSerializer(
            instance=instance.rack,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    def get_item_info(self, instance):
        """ self referral field """
        serializer = WmsItemSerializer(
            instance=instance.item,
            many=True, context={'request': self.context.get("request")}
        )
        return serializer.data

    def get_attachment_info(self, instance):
        """ self referral field """
        serializer = InventoryFileSerializer(
            instance=instance.attachment,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    class Meta:
        model = WmsInventoryCheck
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'is_checked', 'check_time',
                  'check_user', 'check_note', 'number', 'inventory_check_type', 'inventory_check_status',
                  'inventory_check_total', 'warehouse', 'warehouse_info', 'area', 'area_info', 'rack', 'rack_info',
                  'item', 'item_info', 'attachment', 'attachment_info', 'remark', 'url']
