from rest_framework import serializers
from account.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    """
    用户注册接口
    """
    email = serializers.EmailField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2', 'email', 'nickname', 'mobile')
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username'),
            nickname=validated_data.get('nickname', None),
            email=validated_data.get('email', None),
            mobile=validated_data.get('mobile', None),
            is_active=True,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
