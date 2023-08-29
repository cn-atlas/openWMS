from rest_framework import serializers
from api.serializers.base import BaseSerializer
from rest_framework_bulk import BulkSerializerMixin, BulkListSerializer
from WMS.models.check import WmsInventoryCheckDetail
from api.serializers.WMSSerializer.WmsRack import WmsSimpleRackSerializer
from api.serializers.WMSSerializer.WmsItem import WmsItemSerializer
from api.serializers.WMSSerializer.WmsInventoryCheck import WmsSimpleInventoryCheckSerializer


class WmsInventoryCheckDetailSerializer(BulkSerializerMixin, BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''
    rack_info = serializers.SerializerMethodField()
    item_info = serializers.SerializerMethodField()
    inventory_check_info = serializers.SerializerMethodField()

    def get_inventory_check_info(self, instance):
        """ self referral field """
        serializer = WmsSimpleInventoryCheckSerializer(
            instance=instance.inventory_check,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    def get_item_info(self, instance):
        """ self referral field """
        serializer = WmsItemSerializer(
            instance=instance.item,
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

    # def allow_bulk_destroy(self, qs, filtered):
    #     """Don't forget to fine-grain this method"""

    # list_serializer_class = BulkListSerializer

    class Meta:
        list_serializer_class = BulkListSerializer
        update_lookup_field = 'id'
        model = WmsInventoryCheckDetail
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'inventory_check',
                  'inventory_check_info', 'rack', 'rack_info', 'item', 'item_info', 'quantity', 'check_quantity',
                  'remark', 'url']
