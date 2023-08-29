import os
import sys
import django

sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OpenWMS.settings")
django.setup()
from pathlib import Path
from api.filters.base import BaseFilter
from django.db.models.fields import *
from django.db.models.fields.related import *
from mptt.models import TreeForeignKey
from django.contrib.auth.models import AnonymousUser
from tools.code_generator.common import *


class FilterMixin(object):
    '''
    通过 Mixin 定制
    '''

    @property
    def qs(self):
        qs = super().qs
        request_user = getattr(self.request, 'user', None)
        if isinstance(request_user, AnonymousUser):
            return []
        if request_user.is_superuser:
            return qs
        return qs.filter(Q(creator=request_user) | Q(editor=request_user))


# 不生成
# except_fields = {}
# all_filters = dict()
# {<model object>: {"field_name": <field_name>, "method": ["icontains", "exact"]}}

# 定制特殊搜索条件
addition_search_field = {
    # ProductCustomerPrice: {
    #     "price__product__id": ["exact"],
    # },
}

model_filter_mixin = {
    # Sample: (FilterMixin,),
    # Pedigree: (FilterMixin,),
    # PedigreePerson: (FilterMixin,),
    # InternalSample: (FilterMixin,),
    # Order: (FilterMixin,),
    # OrderProduct: (FilterMixin,),
    # # OrderStatus: (FilterMixin,),
    # OrderPayment: (FilterMixin,),
}

# 混入 权限范围 筛选器
# model_range_filter = [
#     # Sample,
# ]

filter_code = """from django_filters import rest_framework as filters
{import_content}


class {filter_name}({filter_class}):
    '''
    DO NOT MODIFY IT!!!
    this ia auto generated from utils.generators.filter
    '''

    class Meta:
        model = {model}
        # 精确过滤字段
        fields = {fields}
        # fields = '__all__'
"""


def do_generate_filters():
    for index, model in enumerate(apps.get_models()):
        if model not in except_models:
            filter_name = model.__name__ + 'Filter'
            dic = dict()
            dic['model'] = model
            dic['fields'] = {}
            # 搜索 fields
            for field in model._meta.fields:
                if isinstance(field, CharField) or isinstance(field, TextField):
                    dic['fields'][field.name] = ['icontains']
                elif isinstance(field, ForeignKey) or isinstance(field, TreeForeignKey):
                    dic['fields'][field.name + "__id"] = ['exact']
                elif isinstance(field, BooleanField) or isinstance(field, IntegerField) \
                        or isinstance(field, BigAutoField) or isinstance(field, BigIntegerField):
                    dic['fields'][field.name] = ['exact']

            if model in addition_search_field:
                for e_field, e_search_method in addition_search_field[model].items():
                    if e_field not in dic['fields']:
                        dic['fields'][e_field] = e_search_method

            xMeta = type('Meta', (object,), dic)
            if model in model_filter_mixin:
                filterset_class = type(filter_name, (*model_filter_mixin[model], BaseFilter), {'Meta': xMeta})
            else:
                filterset_class = type(filter_name, (BaseFilter,), {'Meta': xMeta})
            # 定制特殊筛选器
            # for field in model._meta.fields:
            #     if isinstance(field, DateTimeField):
            #         setattr(filter_class, field.name, DateTimeFromToRangeFilter)
            filter_dir = "{}/api/filters/{}Filter".format(settings.BASE_DIR, model._meta.app_label)
            init_file_path = filter_dir + "/__init__.py"
            if not os.path.exists(filter_dir):
                os.mkdir(filter_dir)
                Path(init_file_path).touch()
            import_content = str(model)
            model_path = import_content.split("'")[1]
            from_path = '.'.join(model_path.split(".")[:len(model_path.split(".")) - 1])
            import_content = "from {} import {}".format(from_path, dic.get("model").__name__)
            filterset_class = "filters.FilterSet"
            # 本项废弃
            # if model in model_range_filter:
            #     filterset_class = "ObjectRangeQSFilterMixin, django_filters.FilterSet"
            filter_file_name = "{}/{}.py".format(filter_dir, model.__name__)
            if not os.path.exists(filter_file_name):
                print("Generating {} file ...".format(filter_file_name))
                with open(filter_file_name, 'w+') as f:
                    f.write(filter_code.format(import_content=import_content, filter_name=filter_name,
                                               filter_class=filterset_class, model=dic.get("model").__name__,
                                               fields=dic.get("fields")))
                with open(init_file_path, "r+") as init_f:
                    import_content = "from api.filters.{}Filter.{} import {}Filter\n".format(model._meta.app_label,
                                                                                             model.__name__,
                                                                                             model.__name__)
                    line_exists = False
                    for line in init_f.readlines():
                        if -1 != import_content.find(line):
                            line_exists = True
                    if not line_exists:
                        init_f.write(import_content)


if __name__ == '__main__':
    do_generate_filters()
