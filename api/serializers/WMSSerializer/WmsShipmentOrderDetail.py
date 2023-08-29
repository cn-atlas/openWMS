from rest_framework import serializers
from api.serializers.base import BaseSerializer
from rest_framework_bulk import BulkSerializerMixin, BulkListSerializer
from WMS.models.shipment import WmsShipmentOrderDetail
# from api.validators.in_out_status import validate_status
from api.serializers.WMSSerializer.WmsShipmentOrder import WmsSimpleShipmentOrderSerializer
from api.serializers.WMSSerializer.WmsRack import WmsRackSerializer
from api.serializers.WMSSerializer.WmsInventory import WmsInventorySerializer


class WmsShipmentOrderDetailSerializer(BulkSerializerMixin, BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''
    shipment_order_info = serializers.SerializerMethodField()
    inventory_info = serializers.SerializerMethodField()
    rack_info = serializers.SerializerMethodField()

    def get_shipment_order_info(self, instance):
        """ self referral field """
        serializer = WmsSimpleShipmentOrderSerializer(
            instance=instance.shipment_order,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    def get_inventory_info(self, instance):
        """ self referral field """
        serializer = WmsInventorySerializer(
            instance=instance.inventory,
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
        list_serializer_class = BulkListSerializer
        update_lookup_field = 'id'
        model = WmsShipmentOrderDetail
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'shipment_order',
                  'shipment_order_info', 'inventory', 'inventory_info', 'plan_quantity', 'real_quantity', 'rack',
                  'rack_info', 'money', 'status', 'remark', 'url']
