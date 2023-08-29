from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from utils.vaptcha import tools as vaptcha_tool
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer


class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request")
        self.fields["token"] = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get("token", None)
        remote_ip = vaptcha_tool.get_client_ip(self.request)
        valid_result = vaptcha_tool.valid_shield(token, remote_ip)
        # 1 为通过，0为失败
        if valid_result.get("success") != 1:
            raise serializers.ValidationError("Captcha {}".format(valid_result.get("msg")))

        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        # if api_settings.UPDATE_LAST_LOGIN:
        update_last_login(None, self.user)

        return data
