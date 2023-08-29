import os
import sys
import django

sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OpenWMS.settings")
django.setup()
from pathlib import Path
from django.conf import settings
from django.db.models.fields import *
from tools.code_generator.common import *

# permission 只是决定有没有权限，对get列表没用
model_permission = {
    # Sample: (IsAuthenticatedCanCreateOwnerOrAdminCanEdit,)
}

pagination_class = {
    # PersonType: NoLimitNumPagination
}

# 权限 model 组，默认是登录可查看，把 model class 写入下面数组，可以对应不同权限, 对应权限需要自定义的，在 utils.permission 里面编写
allow_any_models = [
    # Channel, BannerArticle,
]

addition_search_fields = {
    # Order: ["seller__name", "seller__number"]
}


def get_import_line_serializer(x_model):
    model_str = str(x_model)
    if -1 != model_str.find("django"):
        x_model_path = model_str.split("'")[1]
        x_model_path = x_model_path.split("models")[0]
        x_from_path = x_model_path.split(".")[-2]
    else:
        x_model_path = model_str.split("'")[1]
        x_from_path = x_model_path.split(".")[0]
    data = "from api.serializers.{x_from_path}Serializer.{model_name} import {serializer_name}".format(
        x_from_path=x_from_path, model_name=x_model.__name__,
        serializer_name=x_model.__name__ + "Serializer")
    return data


def get_import_line_filter(x_model):
    model_str = str(x_model)
    if -1 != model_str.find("django"):
        x_model_path = model_str.split("'")[1]
        x_model_path = x_model_path.split("models")[0]
        x_from_path = x_model_path.split(".")[-2]
    else:
        x_model_path = model_str.split("'")[1]
        x_from_path = x_model_path.split(".")[0]
    data = "from api.filters.{x_from_path}Filter.{model_name} import {filter_name}".format(
        x_from_path=x_from_path, model_name=x_model.__name__,
        filter_name=x_model.__name__ + "Filter")
    return data


view_set_template = """from api.views.base import BaseViewSet
{import_content}


class {model_name}ViewSet(BaseViewSet):
    # permission_classes = {permission_classes}
    queryset = {queryset}{pagination_class}
    queryset = queryset.prefetch_related()
    serializer_class = {serializer_class}
    # 这个是在指定字段搜索里面使用, 只支持精确搜索, 必须全部匹配或者使用特殊符号指定搜索方式
    filterset_class = {filter_class}

    # 只有 url?search=russell 使用, 只支持在指定字段里面模糊搜索
    search_fields = {search_fields}
"""


def do_generate_viewsets():
    for model in all_models:
        if model not in except_models:
            view_set_name = model.__name__ + 'ViewSet'
            view_set_dir = "{}/api/views/{}ViewSet".format(settings.BASE_DIR, model._meta.app_label)
            init_file_path = view_set_dir + "/__init__.py"
            view_set_file_name = "{}/{}.py".format(view_set_dir, model.__name__)
            import_content = ""
            import_content += get_import_line(model)
            if not os.path.exists(view_set_dir):
                os.mkdir(view_set_dir)
                Path(init_file_path).touch()
            queryset_str = model.__name__ + ".objects"
            if hasattr(model, "is_show"):
                queryset_str += ".filter(is_show=True)"
            if hasattr(model, "is_checked"):
                queryset_str += ".filter(is_checked=True)"

            if model in allow_any_models:
                permission_classes = "(permissions.AllowAny,)"
                import_content += "\n" + "from rest_framework import permissions"
            elif model in model_permission:
                import_content += "\n" + "from api.utils.permission import *"
                permission_classes = "(" + str(model_permission[model][0].__name__) + ",)"
            else:
                permission_classes = None
                import_content = ""
                # permission_classes = "(permissions.IsAuthenticated,)"
                # import_content += "\n" + "from rest_framework import permissions"
            import_content += "\n" + get_import_line_serializer(model)
            import_content += "\n" + get_import_line_filter(model)
            filterset_class = model.__name__ + "Filter"
            serializer_class = model.__name__ + "Serializer"

            x_pagination_class = ""
            if model in pagination_class:
                from_str = ".".join(str(pagination_class[model]).split("'")[1].split(".")[0:-1])
                import_str = str(pagination_class[model]).split("'")[1].split(".")[-1]
                import_content += "\n" + "from {} import {}".format(from_str, import_str)
                x_pagination_class = "\n    pagination_class = " + import_str

            x_search_fields = []
            for field in model._meta.fields:
                if isinstance(field, CharField) or isinstance(field, TextField):
                    x_search_fields.append(field.name)
            if model in addition_search_fields:
                x_search_fields.extend(addition_search_fields[model])
            search_fields = str(x_search_fields)
            if not os.path.exists(view_set_file_name):
                print("Generating {} file ...".format(view_set_file_name))
                with open(view_set_file_name, 'w+') as f:
                    f.write(view_set_template.format(import_content=import_content, model_name=model.__name__,
                                                     permission_classes=permission_classes,
                                                     # get_sub_field_info_function=get_sub_field_info_function,
                                                     queryset=queryset_str + ".all()",
                                                     pagination_class=x_pagination_class,
                                                     serializer_class=serializer_class, filter_class=filterset_class,
                                                     search_fields=search_fields))

                with open(init_file_path, "r+") as init_f:
                    import_content = "from .{} import {}ViewSet\n".format(
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
    do_generate_viewsets()
