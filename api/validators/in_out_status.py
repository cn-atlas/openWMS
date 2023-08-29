from rest_framework import serializers


def validate_status(cls, attrs):
    """
    状态变更，拦截报错
    注意：不支持 bulk 接口， bulk 的 instance 是 queryset

    :param cls: 序列化器验证器对象
    :param attrs: 序列化器 attrs 包含 提交上来的数据
    :return:
    """
    if "status" in attrs:
        if attrs.get("status") < -2 or attrs.get("status") > 3:
            raise serializers.ValidationError("状态码非法，请检查！")
        if cls.instance:
            if cls.instance.status != attrs.get("status") and cls.instance.status > 1 and attrs.get("status") > 1:
                raise serializers.ValidationError("这两个状态不支持切换！")
    return attrs
