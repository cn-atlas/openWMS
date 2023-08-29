from rest_framework import serializers
from api.serializers.base import BaseSerializer
from account.models.department import Department


class DepartmentSerializer(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''

    class Meta:
        model = Department
        fields = ['id', 'is_show', 'create_time', 'edit_time', 'creator', 'editor', 'parent', 'company',
                  'department_number', 'department_name', 'remark', 'lft', 'rght', 'tree_id', 'level', 'group', 'url']
