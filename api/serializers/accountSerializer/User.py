from rest_framework import serializers
from api.serializers.base import BaseSerializer
from account.models.user import User


class MiniUserSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        '''
        信息比较敏感，只能使用 fields 而不能使用 exclude
        '''
        fields = ["id", "username", "nickname", 'first_name', 'email', 'url']
        model = User


class SimpleUserSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        '''
        信息比较敏感，只能使用 fields 而不能使用 exclude
        '''
        fields = ["id", "username", "nickname", "mobile", 'first_name']
        model = User


class UserSerializer(SimpleUserSerializer):
    company_info = serializers.SerializerMethodField()
    department_info = serializers.SerializerMethodField()

    def get_company_info(self, instance):
        from api.serializers.accountSerializer.Company import CompanySerializer
        """ self referral field """
        serializer = CompanySerializer(
            instance=instance.company,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    def get_department_info(self, instance):
        from api.serializers.accountSerializer.Department import DepartmentSerializer
        """ self referral field """
        serializer = DepartmentSerializer(
            instance=instance.department,
            many=False, context={'request': self.context.get("request")}
        )
        return serializer.data

    class Meta(BaseSerializer.Meta):
        '''
        信息比较敏感，只能使用 fields 而不能使用 exclude
        '''
        fields = ["url", "id", "is_superuser", "username", "user_code", "title", "email", "nickname", "mobile",
                  "description", "job_number", "gender", "company", "company_info", "department", "department_info",
                  "icon", 'first_name']
        model = User
