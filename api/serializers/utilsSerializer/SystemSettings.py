from rest_framework import serializers
from api.serializers.base import BaseSerializer
from utils.models.system_info import SystemSettings


class SystemSettingsSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''
     
    class Meta:
        model = SystemSettings
        fields = ['id', 'site_name', 'short_site_name', 'copy_right_company_name', 'system_name', 'record', 'record_link', 'version', 'other_info', 'small_logo', 'big_logo', 'other_icon', 'url'] 
