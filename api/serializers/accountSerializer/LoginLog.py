from rest_framework import serializers
from api.serializers.base import BaseSerializer
from account.models.user import LoginLog


class LoginLogSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''
     
    class Meta:
        model = LoginLog
        fields = ['id', 'credential', 'method', 'login_username', 'ip', 'city', 'agent', 'remark', 'status', 'login_time', 'url'] 
