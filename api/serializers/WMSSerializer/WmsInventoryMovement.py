from rest_framework import serializers
from api.serializers.base import BaseSerializer
from WMS.models.movement import WmsInventoryMovement
from api.validators.in_out_status import validate_status
from api.serializers.WMSSerializer.WmsRack import WmsRackSerializer


class WmsSimpleInventoryMovementSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    def validate(self, attrs):
        return validate_status(self, attrs)

    class Meta:
        model = WmsInventoryMovement
        fields = ['id', 'is_checked', 'number', 'status', 'remark', 'url']


class WmsInventoryMovementSerializer(WmsSimpleInventoryMovementSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    source_rack_info = serializers.SerializerMethodField()
    target_rack_info = serializers.SerializerMethodField()

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

    class Meta:
        model = WmsInventoryMovement
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'is_checked', 'check_time',
                  'check_user', 'check_note', 'number', 'source_rack', 'target_rack', 'source_rack_info',
                  'target_rack_info', 'status', 'remark', 'url']
