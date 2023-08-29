from rest_framework import serializers
from api.serializers.base import BaseSerializer
from api.serializers.WMSSerializer.WmsAbsItem import WmsSimpleAbsItemSerializer
from WMS.models.item import WmsItem


class WmsItemSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    abs_item_info = serializers.SerializerMethodField()

    def get_abs_item_info(self, instance):
        """ self referral field """
        serializer = WmsSimpleAbsItemSerializer(
            instance=instance.abs_item,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    class Meta:
        model = WmsItem
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'abs_item', 'abs_item_info',
                  'batch_number', 'produce_date', 'expiry_date', 'remark', 'url']
