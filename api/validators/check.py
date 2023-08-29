from rest_framework import serializers


def validate_non(cls, attrs):
    """
    验证四选一
    注意：不支持 bulk 接口， bulk 的 instance 是 queryset

    :param cls: 序列化器验证器对象
    :param attrs: 序列化器 attrs 包含 提交上来的数据
    :return:
    """
    # 新增时候
    if not cls.instance:
        if "inventory_check_type" not in attrs or attrs.get("inventory_check_type", None) is None:
            raise serializers.ValidationError("盘库类型必填！")
        if attrs.get("inventory_check_type", -1) == 0:
            if "warehouse" not in attrs or attrs.get("warehouse", None) is None:
                raise serializers.ValidationError("盘库类型不符！")
        elif attrs.get("inventory_check_type", -1) == 1:
            if "area" not in attrs or attrs.get("area", None) is None:
                raise serializers.ValidationError("盘库类型不符！")
        elif attrs.get("inventory_check_type", -1) == 2:
            if "rack" not in attrs or attrs.get("rack", None) is None:
                raise serializers.ValidationError("盘库类型不符！")
        elif attrs.get("inventory_check_type", -1) == 3:
            if "item" not in attrs or not attrs.get("item"):
                raise serializers.ValidationError("盘库类型不符！")
    return attrs
