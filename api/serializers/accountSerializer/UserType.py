from rest_framework import serializers
from api.serializers.base import BaseSerializer
from account.models.user import UserType


class UserTypeSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''
     
    class Meta:
        model = UserType
        fields = ['id', 'name', 'remark', 'url'] 
