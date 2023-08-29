from rest_framework import serializers
from api.serializers.base import BaseSerializer
from WMS.models.shipment import WmsDelivery
from api.serializers.WMSSerializer.WmsShipmentOrder import WmsSimpleShipmentOrderSerializer


class WmsDeliverySerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''
    shipment_order_info = serializers.SerializerMethodField()

    def get_shipment_order_info(self, instance):
        """ self referral field """
        serializer = WmsSimpleShipmentOrderSerializer(
            instance=instance.shipment_order,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    class Meta:
        model = WmsDelivery
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'shipment_order',
                  'shipment_order_info', 'carrier', 'delivery_date', 'tracking_no', 'remark', 'url']
