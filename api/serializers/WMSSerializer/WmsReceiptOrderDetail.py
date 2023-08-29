from rest_framework import serializers
from api.serializers.base import BaseSerializer
from WMS.models.receipt import WmsReceiptOrderDetail
# from api.validators.in_out_status import validate_status
from rest_framework_bulk import BulkSerializerMixin, BulkListSerializer
from api.serializers.WMSSerializer.WmsReceiptOrder import WmsSimpleReceiptOrderSerializer
from api.serializers.WMSSerializer.WmsItem import WmsItemSerializer
from api.serializers.WMSSerializer.WmsRack import WmsRackSerializer


class WmsReceiptOrderDetailSerializer(BulkSerializerMixin, BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''
    receipt_order_info = serializers.SerializerMethodField()
    item_info = serializers.SerializerMethodField()
    rack_info = serializers.SerializerMethodField()

    def get_receipt_order_info(self, instance):
        """ self referral field """
        serializer = WmsSimpleReceiptOrderSerializer(
            instance=instance.receipt_order,
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
        serializer = WmsRackSerializer(
            instance=instance.rack,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    # def validate(self, attrs):
    #     return validate_status(self, attrs)

    class Meta:
        model = WmsReceiptOrderDetail
        list_serializer_class = BulkListSerializer
        update_lookup_field = 'id'
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'receipt_order',
                  'receipt_order_info', 'item', 'item_info', 'plan_quantity', 'real_quantity', 'rack', 'rack_info',
                  'money', 'status', 'remark', 'url']
