from rest_framework import serializers
from api.serializers.base import BaseSerializer
from WMS.models.shipment import WmsShipmentOrder
from api.validators.in_out_status import validate_status
from api.serializers.accountSerializer.User import MiniUserSerializer


class WmsSimpleShipmentOrderSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    def validate(self, attrs):
        return validate_status(self, attrs)

    class Meta:
        model = WmsShipmentOrder
        fields = ['id', 'is_checked', 'check_time', 'number', 'shipment_order_type', 'to_customer',
                  'to_user', 'receivable_amount', 'status', 'remark', 'url']


class WmsShipmentOrderSerializer(WmsSimpleShipmentOrderSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    to_user_info = serializers.SerializerMethodField()

    def get_to_user_info(self, instance):
        """ self referral field """
        serializer = MiniUserSerializer(
            instance=instance.to_user,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    class Meta:
        model = WmsShipmentOrder
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'is_checked', 'check_time',
                  'check_user', 'check_note', 'number', 'shipment_order_type', 'order_no', 'to_customer',
                  'to_user', 'to_user_info', 'receivable_amount', 'status', 'remark', 'url']
