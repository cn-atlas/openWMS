from rest_framework import serializers
from api.serializers.base import BaseSerializer
from api.serializers.WMSSerializer.WmsItemType import WmsSimpleItemTypeSerializer
from WMS.models.item import WmsAbsItem


class WmsSimpleAbsItemSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    class Meta:
        model = WmsAbsItem
        fields = ['id', 'number', 'name', 'specs', 'model', 'unit', 'manufacturer', 'total_number', 'remark', 'url']


class WmsAbsItemSerializer(WmsSimpleAbsItemSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''
    item_type_info = serializers.SerializerMethodField()

    def get_item_type_info(self, instance):
        """ self referral field """
        serializer = WmsSimpleItemTypeSerializer(
            instance=instance.item_type,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    class Meta:
        model = WmsAbsItem
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'number', 'name', 'specs', 'model',
                  'item_type', 'item_type_info', 'unit', 'manufacturer', 'quantity', 'total_number', 'remark', 'url']
