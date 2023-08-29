import os
import sys
import django
from pathlib import Path
from django.conf import settings
from django.db.models.fields import *
from tools.code_generator.common import *

sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PrecisionReport.settings")
django.setup()


class DRFViewSetGenerator:
    def __init__(self):
        self.model_permission = {}
        self.pagination_class = {}
        self.allow_any_models = []
        self.addition_search_fields = {}

    def split_text(self, text, line_length):
        return [text[i:i + line_length] for i in range(0, len(text), line_length)]

    def get_import_line(self, x_model, module_type):
        model_str = str(x_model)
        if -1 != model_str.find("django"):
            x_model_path = model_str.split("'")[1]
            x_model_path = x_model_path.split("models")[0]
            x_from_path = x_model_path.split(".")[-2]
        else:
            x_model_path = model_str.split("'")[1]
            x_from_path = x_model_path.split(".")[0]
        module_path = "api.serializers" if module_type == "serializer" else "api.filters"
        data = "from {}.{}.{} import {}".format(module_path, x_from_path, model_name, serializer_filter_name)
        return data

    def generate_viewsets(self):
        view_set_template = """from api.views.base import BaseViewSet
{import_content}

class {model_name}ViewSet(BaseViewSet):
    permission_classes = {permission_classes}
    queryset = {queryset}{pagination_class}
    queryset = queryset.prefetch_related()
    serializer_class = {serializer_class}
    filterset_class = {filter_class}
    search_fields = {search_fields}
"""

        for model in all_models:
            if model not in except_models:
                view_set_name = model.__name__ + 'ViewSet'
                view_set_dir = "{}/api/views/{}ViewSet".format(settings.BASE_DIR, model._meta.app_label)
                init_file_path = view_set_dir + "/__init__.py"
                view_set_file_name = "{}/{}.py".format(view_set_dir, model.__name__)
                import_content = ""
                import_content += self.get_import_line(model, "serializer")
                import_content += "\n" + self.get_import_line(model, "filter")

                if not os.path.exists(view_set_dir):
                    os.mkdir(view_set_dir)
                    Path(init_file_path).touch()

                queryset_str = model.__name__ + ".objects.all()"
                if hasattr(model, "is_show"):
                    queryset_str += ".filter(is_show=True)"
                if hasattr(model, "is_checked"):
                    queryset_str += ".filter(is_checked=True)"

                if model in self.allow_any_models:
                    permission_classes = "(permissions.AllowAny,)"
                    import_content += "\n" + "from rest_framework import permissions"
                elif model in self.model_permission:
                    import_content += "\n" + "from api.utils.permission import *"
                    permission_classes = "(" + str(self.model_permission[model][0].__name__) + ",)"
                else:
                    permission_classes = "(permissions.IsAuthenticated,)"
                    import_content += "\n" + "from rest_framework import permissions"

                filterset_class = model.__name__ + "Filter"
                serializer_class = model.__name__ + "Serializer"

                x_pagination_class = ""
                if model in self.pagination_class:
                    pagination_class_name = str(self.pagination_class[model]).split("'")[1].split(".")[-1]
                    import_content += "\n" + "from {} import {}".format(
                        ".".join(str(self.pagination_class[model]).split("'")[1].split(".")[0:-1], pagination_class_name)
                    x_pagination_class = "\n    pagination_class = " + pagination_class_name

                x_search_fields = []
                for field in model._meta.fields:
                    if isinstance(field, CharField) or isinstance(field, TextField):
                        x_search_fields.append(field.name)
                if model in self.addition_search_fields:
                    x_search_fields.extend(self.addition_search_fields[model])
                search_fields = str(x_search_fields)

                if not os.path.exists(view_set_file_name):
                    with open(view_set_file_name, 'w+') as f:
                        f.write(view_set_template.format(import_content=import_content, model_name=model.__name__,
                                                         permission_classes=permission_classes,
                                                         queryset=queryset_str,
                                                         pagination_class=x_pagination_class,
                                                         serializer_class=serializer_class,
                                                         filter_class=filter_class,
                                                         search_fields=search_fields))

                    with open(init_file_path, "r+") as init_f:
                        import_content = "from .{} import {}ViewSet\n".format(model.__name__, model.__name__)
                        line_exists = False
                        for line in init_f.readlines():
                            if -1 != import_content.find(line):
                                line_exists = True
                        if not line_exists:
                            init_f.write(import_content)

