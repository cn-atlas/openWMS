from api.serializers.base import BaseSerializer
from WMS.models.receipt import WmsReceiptOrder
from api.validators.in_out_status import validate_status


class WmsSimpleReceiptOrderSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    def validate(self, attrs):
        return validate_status(self, attrs)

    class Meta:
        model = WmsReceiptOrder
        fields = ['id', 'number', 'receipt_type', 'status', 'remark', 'url']


class WmsReceiptOrderSerializer(WmsSimpleReceiptOrderSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    class Meta:
        model = WmsReceiptOrder
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'number', 'receipt_type',
                  'supplier', 'order_no', 'payable_amount', 'status', 'remark', 'url']
