from rest_framework import serializers
from api.serializers.base import BaseSerializer
# from api.validators.in_out_status import validate_status
from rest_framework_bulk import BulkSerializerMixin, BulkListSerializer
from api.serializers.WMSSerializer.WmsInventoryMovement import WmsSimpleInventoryMovementSerializer
from WMS.models.movement import WmsInventoryMovementDetail
from api.serializers.WMSSerializer.WmsRack import WmsRackSerializer
from api.serializers.WMSSerializer.WmsInventory import WmsInventorySerializer


class WmsInventoryMovementDetailSerializer(BulkSerializerMixin, BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''
    status = serializers.IntegerField(read_only=True)
    inventory_movement_info = serializers.SerializerMethodField()
    inventory_info = serializers.SerializerMethodField()
    source_rack_info = serializers.SerializerMethodField()
    target_rack_info = serializers.SerializerMethodField()

    def get_inventory_movement_info(self, instance):
        """ self referral field """
        serializer = WmsSimpleInventoryMovementSerializer(
            instance=instance.inventory_movement,
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

    def get_source_rack_info(self, instance):
        """ self referral field """
        serializer = WmsRackSerializer(
            instance=instance.source_rack,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    def get_target_rack_info(self, instance):
        """ self referral field """
        serializer = WmsRackSerializer(
            instance=instance.target_rack,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    # def validate(self, attrs):
    #     return validate_status(self, attrs)

    class Meta:
        list_serializer_class = BulkListSerializer
        update_lookup_field = 'id'
        model = WmsInventoryMovementDetail
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'inventory_movement',
                  'inventory_movement_info', 'inventory', 'inventory_info', 'plan_quantity', 'real_quantity',
                  'source_rack', 'target_rack', 'source_rack_info', 'target_rack_info', 'status', 'remark', 'url']
