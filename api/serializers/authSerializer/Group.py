from rest_framework import serializers
from api.serializers.base import BaseSerializer
from django.contrib.auth.models import Group


class GroupSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''
     
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions', 'url'] 
