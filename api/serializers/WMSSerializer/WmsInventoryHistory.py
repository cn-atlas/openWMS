from rest_framework import serializers
from api.serializers.base import BaseSerializer
from api.serializers.WMSSerializer import WmsItemSerializer
from api.serializers.WMSSerializer.WmsRack import WmsRackSerializer
from api.serializers.WMSSerializer.WmsReceiptOrder import WmsSimpleReceiptOrderSerializer
from api.serializers.WMSSerializer.WmsShipmentOrder import WmsSimpleShipmentOrderSerializer
from api.serializers.WMSSerializer.WmsInventoryMovement import WmsSimpleInventoryMovementSerializer
from WMS.models.inventory import WmsInventoryHistory


class WmsInventoryHistorySerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    item_info = serializers.SerializerMethodField()
    rack_info = serializers.SerializerMethodField()
    inventory_movement_info = serializers.SerializerMethodField()
    inventory_receipt_order_info = serializers.SerializerMethodField()
    inventory_shipment_order_info = serializers.SerializerMethodField()
    balance = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)

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

    def get_inventory_movement_info(self, instance):
        """ self referral field """
        serializer = WmsSimpleInventoryMovementSerializer(
            instance=instance.inventory_movement,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    def get_inventory_receipt_order_info(self, instance):
        """ self referral field """
        serializer = WmsSimpleReceiptOrderSerializer(
            instance=instance.inventory_receipt_order,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    def get_inventory_shipment_order_info(self, instance):
        """ self referral field """
        serializer = WmsSimpleShipmentOrderSerializer(
            instance=instance.inventory_shipment_order,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    class Meta:
        model = WmsInventoryHistory
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'inventory_movement',
                  'inventory_receipt_order', 'inventory_shipment_order', 'form_type', 'number_type', 'item',
                  'item_info', 'rack', 'rack_info', 'quantity', 'balance', 'remark', 'url', 'inventory_movement_info',
                  'inventory_receipt_order_info', 'inventory_shipment_order_info']
