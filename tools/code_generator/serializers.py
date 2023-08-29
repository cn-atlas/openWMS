import os
import sys
import django

sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OpenWMS.settings")
django.setup()
from pathlib import Path
import copy
from django.db.models.fields.related import *
from api.serializers.base import BaseSerializer
from tools.code_generator.common import *

# ForeignKey 嵌入
embed_obj_serializer = {
    # ProductCustomerPrice: ["price"],
    # ProductSellerPrice: ["price"],
    # BannerArticle: ["big_image", "image", "video"],
    # # Order: {"order_orderpedigree", "order_ordersmple", "order_orderpayment"},
    # # 缺少的信息   检测产品    收样时间   销售 送检客户   样本类型     样本状态    产品的正常的周期时长，用于计算预计结束时间 结算状态
    # # Sample: ["gender"],
    # OrderProduct: ["product"],
    # OrderPayment: ["status"],
    # Product: ["cover_img"],
    # SampleAdditionValue: ["info"],
    # PedigreePerson: ["sample", "person_type"],
    # NewsArticle: ["big_image", "image", "video"],
}

# 获取包含外键 related_name 的所有 field
# meta_fields_with_related_names = {Order: [field.name for field in Order._meta.get_fields()]}
# related name 嵌入 __str__ 内容
# 编写规范： {model: {related_name: is_many}}
addition_str_fields = {
    # Order: {
    #     'order_ordersample': True,
    #     'order_orderpedigree': True,
    #     'order_orderproduct': True,
    #     'order_orderpayment': False
    # }
}

# related name 嵌入 Serializer 内容，慎用，因为可能出现还没有生成子 Serializer 的情况导致崩溃, 由于是嵌套加载也会变慢
# 编写规范： {model: {related_name: {}}}}
addition_detail_fields = {
}

get_sub_field_info_function_str = '''
    def get_{field_name}_info(self, instance):
        """ self referral field """
        serializer = {sub_obj_serializer}(
            instance=instance.{field_name},
            many={is_many_str}, context={{'request': self.context.get("request")}}
        )
        return serializer.data
'''


def fill_fields(x_model, model_fields, dic):
    if x_model in model_fields:
        if isinstance(dic['fields'], list):
            dic['fields'] = dic['fields'] + list(model_fields[x_model].keys())
        else:
            dic['fields'] = [field.name for field in x_model._meta.fields] + list(model_fields[x_model].keys())
        if "url" not in dic['fields']:
            dic['fields'] += ["url"]


def get_import_line_serializer(x_model):
    model_str = str(x_model)
    # print(model_str)
    x_model_path = model_str.split("'")[1]
    x_from_path = x_model_path.split(".")[0]
    data = "from api.serializers.{x_from_path}Serializer.{model_name} import {serializer_name}".format(
        x_from_path=x_from_path, model_name=x_model.__name__,
        serializer_name=x_model.__name__ + "Serializer")
    return data


filter_code = """from rest_framework import serializers
from api.serializers.base import BaseSerializer
{import_content}


class {serializer_name}(BaseSerializer):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.serializer
    '''
    {get_sub_field} 
    class Meta:
        model = {model}
        fields = {fields} 
"""


def do_generate_serializers():
    # 所有序列化起生成结束才可以额外补充属性
    for model in all_models:
        if model not in except_models:
            attr_dic = dict()
            dic = copy.deepcopy({
                k: v
                for (k, v) in BaseSerializer.Meta.__dict__.items()
                if not k.startswith('__')
            })

            serializer_dir = "{}/api/serializers/{}Serializer".format(settings.BASE_DIR, model._meta.app_label)

            init_file_path = serializer_dir + "/__init__.py"
            serializer_name = model.__name__ + 'Serializer'
            import_content = get_import_line(model)
            serializer_file_name = "{}/{}.py".format(serializer_dir, model.__name__)

            #  构造整个 Meta 属性
            dic['model'] = model.__name__
            fill_fields(model, addition_str_fields, dic)
            fill_fields(model, addition_detail_fields, dic)
            addition_fields = []

            if model in embed_obj_serializer:
                added_related_models = []
                for field_name in embed_obj_serializer.get(model):
                    is_many_str = "True" if isinstance(model._meta.get_field(field_name), ManyToManyField) else "False"
                    attr_dic[field_name + "_info"] = "serializers.SerializerMethodField(read_only=True)"

                    # import_content += "\n" + field_name + "Serializer"
                    related_model = model._meta.get_field(field_name).remote_field.model
                    # print(related_model)
                    related_model_serializer = related_model.__name__ + "Serializer"
                    get_import_line_serializer(related_model)
                    if related_model not in added_related_models:
                        import_line = get_import_line_serializer(related_model)
                        if import_content == "":
                            import_content = import_line
                        else:
                            import_content += "\n" + import_line
                        # print(import_line)
                        # print()
                        added_related_models.append(related_model)
                    # print(model, model._meta.get_field(field_name).remote_field.model.__name__, type(model._meta.get_field(field_name)), related_model)
                    # print(related_model_serializer)
                    x_get_sub_field_info_function_str = get_sub_field_info_function_str.format(
                        sub_obj_serializer=related_model_serializer,
                        field_name=field_name, is_many_str=is_many_str)
                    # foo_func = FunctionType(compile(x_get_sub_field_info_function_str, "<string>", "exec").co_consts[0],
                    #                         locals(), "get_{field_name}_info".format(field_name=field_name))
                    attr_dic["get_{field_name}_info".format(field_name=field_name)] = x_get_sub_field_info_function_str
                    addition_fields.append("{field_name}_info".format(field_name=field_name))
            if model in addition_str_fields:
                for related_field_name, is_many in addition_str_fields.get(model).items():
                    attr_dic[related_field_name] = "serializers.StringRelatedField(many={}, read_only=True)".format(
                        "True" if is_many else "False")
                    addition_fields.append(related_field_name)
            # if model in addition_detail_fields:
            #     for related_field_name, content in addition_detail_fields.get(model).items():
            #         attr_dic[related_field_name] = all_serializers.get(content.get("model"))(many=content.get("many"),
            #                                                                                  read_only=True)

            # print(dic, attr_dic)
            if not os.path.exists(serializer_dir):
                os.mkdir(serializer_dir)
                Path(init_file_path).touch()
                # with open(serializer_dir + "/__init__.py", "w+") as f:
                #     f.write()
            get_sub_field = ""
            for k, v in attr_dic.items():
                if not k.startswith("get_"):
                    get_sub_field += "\n    {} = {}".format(k, v)
            for k, v in attr_dic.items():
                if k.startswith("get_"):
                    get_sub_field += "\n" + v
            # if not os.path.exists(serializer_file_name):
            # [field.name for field in model._meta.get_all_related_many_to_many_objects()] \
            all_fields = [field.name for field in model._meta.fields] + \
                         [field.name for field in model._meta.many_to_many] + ["url"] \
                if dic.get("fields") == "__all__" else dic.get("fields")
            # all_fields = model._meta.get_all_field_names() if dic.get("fields") == "__all__" else dic.get("fields")
            for field in addition_fields:
                if field not in all_fields:
                    all_fields.append(field)
            if not os.path.exists(serializer_file_name):
                print("Generating {} file ...".format(serializer_file_name))
                with open(serializer_file_name, 'w+') as f:
                    f.write(filter_code.format(import_content=import_content, serializer_name=serializer_name,
                                               get_sub_field=get_sub_field,
                                               # get_sub_field_info_function=get_sub_field_info_function,
                                               model=model.__name__,
                                               fields=all_fields,
                                               exclude_fields=""))

                with open(init_file_path, "r+") as init_f:
                    import_content = "from .{} import {}Serializer\n".format(
                        # model._meta.app_label,
                        model.__name__,
                        model.__name__)
                    line_exists = False
                    for line in init_f.readlines():
                        if -1 != import_content.find(line):
                            line_exists = True
                    if not line_exists:
                        init_f.write(import_content)


if __name__ == '__main__':
    do_generate_serializers()
