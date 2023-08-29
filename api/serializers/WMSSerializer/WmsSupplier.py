from rest_framework import serializers
from api.serializers.base import BaseSerializer
from WMS.models.receipt import WmsSupplier


class WmsSupplierSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    class Meta:
        model = WmsSupplier
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'number', 'name', 'bank_name',
                  'bank_account', 'address', 'mobile_no', 'tel_no', 'contact', 'level', 'email', 'remark', 'item',
                  'url']
