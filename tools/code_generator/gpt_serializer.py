import os
import sys
import django

sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PrecisionReport.settings")
django.setup()
from pathlib import Path
import copy
from django.db.models.fields.related import *
from api.serializers.base import BaseSerializer
from tools.code_generator.common import *


class DRFSerializerGenerator:
    def __init__(self, model):
        self.model = model
        self.serializer_name = model.__name__ + 'Serializer'
        self.fields = {}

    def generate_serializer(self):
        import_content = self._get_import_line()

        self._fill_fields(addition_str_fields)
        self._fill_fields(addition_detail_fields)

        addition_fields = []
        get_sub_field_info_functions = []

        if self.model in embed_obj_serializer:
            for field_name in embed_obj_serializer.get(self.model):
                is_many = isinstance(self.model._meta.get_field(field_name), ManyToManyField)
                attr_name = field_name + "_info"
                attr_value = "serializers.SerializerMethodField(read_only=True)"
                self.fields[attr_name] = attr_value

                related_model = self.model._meta.get_field(field_name).remote_field.model
                related_model_serializer = related_model.__name__ + "Serializer"
                get_sub_field_info_function = self._generate_get_sub_field_info_function(
                    related_model_serializer, field_name, is_many)
                get_sub_field_info_functions.append(get_sub_field_info_function)

                addition_fields.append(attr_name)

        if self.model in addition_str_fields:
            for related_field_name, is_many in addition_str_fields.get(self.model).items():
                attr_name = related_field_name
                attr_value = "serializers.StringRelatedField(many={}, read_only=True)".format(
                    "True" if is_many else "False")
                self.fields[attr_name] = attr_value
                addition_fields.append(attr_name)

        serializer_code = f'''from rest_framework import serializers
from api.serializers.base import BaseSerializer
{import_content}


class {self.serializer_name}(BaseSerializer):
    {"".join(get_sub_field_info_functions)}

    class Meta:
        model = {self.model.__name__}
        fields = {list(self.fields.keys())}
'''

        return serializer_code

    def _get_import_line(self):
        model_str = str(self.model)
        x_model_path = model_str.split("'")[1]
        x_from_path = x_model_path.split(".")[0]
        import_line = "from api.serializers.{x_from_path}Serializer.{model_name} import {serializer_name}".format(
            x_from_path=x_from_path, model_name=self.model.__name__,
            serializer_name=self.model.__name__ + "Serializer")
        return import_line

    def _fill_fields(self, field_dict):
        if self.model in field_dict:
            for related_field_name, value in field_dict.get(self.model).items():
                self.fields[related_field_name] = value

    def _generate_get_sub_field_info_function(self, sub_obj_serializer, field_name, is_many):
        return f'''
    def get_{field_name}_info(self, instance):
        serializer = {sub_obj_serializer}(
            instance=instance.{field_name},
            many={is_many}, context={{'request': self.context.get("request")}}
        )
        return serializer.data
'''


# 示例用法
serializer_generator = DRFSerializerGenerator(YourModel)
serializer_code = serializer_generator.generate_serializer()
print(serializer_code)
