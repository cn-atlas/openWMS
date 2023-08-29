import json
import os
import sys
import random
import django
from faker import Faker
from pathlib import Path
from django.apps import apps

sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OpenWMS.settings")
django.setup()

from django.conf import settings
from mptt.models import MPTTModelBase
from OpenWMS.base_model import models, BaseMPTTModel

fake = Faker(["zh-CN"])
# Step 1: Define the test case class template
test_case_template = """import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.{app_name}ViewSet import {model}ViewSet
from api.filters.{app_name}Filter import {model}Filter
from api.tests.{app_name}Tests import common
{import_content}
import logging

logger = logging.getLogger(__name__)


class {model}Tests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        self.test_data = {field_mapping}
        self.update_data = {update_field_mapping}
        
        url = reverse('{lower_model_name}-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual({model}.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr({model}.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = {model}.objects.get()

    def test_get_{lower_model_name}_list(self):
        url = reverse('{lower_model_name}-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_{lower_model_name}(self):
        url = reverse('{lower_model_name}-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = {model}.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr({model}.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('{lower_model_name}-list')
        search_key = random.choice({model}ViewSet.search_fields)
        k = self.update_data.get(search_key, None) if not self.update_data.get(search_key, None) else \
        self.test_data.get(search_key, "")
        full_url = url + "?search=" + k
        response = self.client.get(full_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_filter(self):
        pass
        
    def tearDown(self) -> None:
        pass
"""


def generate_random_str(random_length=16):
    """
    生成随机字符串
    :param random_length: 字符串长度
    :return:
    """
    strs = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    x_random = random.Random()
    for i in range(random_length):
        strs += chars[x_random.randint(0, length)]
    return strs


def generate_random_data(field):
    if isinstance(field, models.BooleanField):
        return True if field.name == "is_show" else random.choice([True, False])

    # if field.primary_key or isinstance(field, models.AutoField) or isinstance(field, models.BigAutoField):
    #     return None  # Skip generating data for the primary key field
    if isinstance(field, models.CharField) and field.name == "name":
        return fake.name()

    if isinstance(field, models.CharField) and (-1 != field.name.find("mobile") or -1 != field.name.find("tel_no")):
        return fake.phone_number()

    if isinstance(field, models.CharField) and -1 != field.name.find("mail"):
        return fake.email()

    if isinstance(field, models.CharField) and (-1 != field.name.find("number") or -1 != field.name.find("code")):
        return generate_random_str(10)

    if isinstance(field, models.CharField):
        if field.max_length < 5:
            return generate_random_str(field.max_length)
        return fake.text(max_nb_chars=random.randint(5, 10 if field.max_length > 10 else field.max_length)) \
            .replace("\n", "")

    if isinstance(field, models.TextField):
        return fake.text().replace("\n", "")

    if isinstance(field, models.EmailField):
        return fake.email()

    if isinstance(field, models.DateTimeField):
        return fake.date_of_birth().strftime('%Y-%m-%d %H:%M:%S')

    if isinstance(field, models.DateField):
        return fake.date_of_birth().strftime('%Y-%m-%d')

    if isinstance(field, models.IntegerField) or isinstance(field, models.PositiveIntegerField) \
            or isinstance(field, models.SmallIntegerField):
        return random.randint(1, 100)

    if isinstance(field, models.FloatField):
        return float(random.randint(1, 100)) / 100

    if isinstance(field, models.DecimalField):
        return float(random.randint(1, 100))

    else:
        return None


# from WMS.models.item import {model}

# Step 2: Get a list of all Django models
# x_models = apps.get_models()
# x_models = [{model}]
# Replace 'myapp' with the actual app label you want to get models for
# 如果直接使用 apps.get_models() 会包含系统默认 model 而这些 model 暂时不参与测试
app_labels = ['WMS']

# Get models for the specified app
for app_label in app_labels:
    app_models = apps.all_models[app_label]

    app = apps.get_app_config(app_label)
    # print(app.module.__path__)
    # app_directory_path = app.module.__path__[0]
    tests_dir = os.path.join(settings.BASE_DIR, "api/tests", f'{app.name}Tests')
    # print(tests_dir)
    #
    # Step 3: Generate test cases for each model
    for _, model in app_models.items():
        meta_class = model.__class__
        # 注意⚠️：中文环境下适用，且注意自己写的表 verbose_name 包含"关系"字样的会跳过生成
        # 这一行为了排除 m2m 虚拟表生成测试，暂时不支持自动化为虚拟表生成测试用例
        if -1 == model._meta.verbose_name.find("关系"):
            # M2M 表暂时不测试
            # if not model._meta.many_to_many:
            model_name = model.__name__
            from django.db.models import Model

            field_mapping = dict()
            test_key = []
            update_field_mapping = {}

            import_content = str(model)
            model_path = import_content.split("'")[1]
            from_path = '.'.join(model_path.split(".")[:len(model_path.split(".")) - 1])
            import_content = "from {} import {}".format(from_path, model_name)

            # Generate field mapping for each field
            for field in model._meta.fields:
                if field.name == "id":
                    continue
                if meta_class == MPTTModelBase and field.name in ["tree_id", "parent", "lft", "rght", "level"]:
                    continue
                field_type = field.get_internal_type()

                if isinstance(field, models.CharField) or isinstance(field, models.TextField) \
                        or isinstance(field, models.EmailField) or isinstance(field, models.DateField) \
                        or isinstance(field, models.DateTimeField):
                    field_mapping[field.name] = generate_random_data(field)
                else:
                    field_mapping[field.name] = generate_random_data(field)
                #  时间格式还要转换，不参与测试, 外键、m2m 手动编写，不自动生成
                if not any([isinstance(field, models.DateTimeField),
                            isinstance(field, models.DateField),
                            isinstance(field, models.ForeignKey),
                            isinstance(field, models.ManyToManyField),
                            field.name == "is_show"]):
                    update_field_mapping[field.name] = generate_random_data(field)

            # field_mapping = json.dumps(field_mapping)
            test_case = test_case_template.format(model=model_name, field_mapping=field_mapping,
                                                  update_field_mapping=update_field_mapping,
                                                  import_content=import_content,
                                                  lower_model_name=model_name.lower(), app_name=app.name)

            init_file_path = tests_dir + "/__init__.py"
            if not os.path.exists(tests_dir):
                os.mkdir(tests_dir)
                Path(init_file_path).touch()

            test_file_name = "{}/{}TestCase.py".format(tests_dir, model.__name__)
            # if not os.path.exists(test_file_name):
            print("Generating {} file ...".format(test_file_name))
            with open(test_file_name, 'w+') as f:
                f.write(test_case)
            with open(init_file_path, "r+") as init_f:
                import_content = f"from .{model_name}TestCase import *\n"
                line_exists = False
                for line in init_f.readlines():
                    if -1 != import_content.find(line):
                        line_exists = True
                if not line_exists:
                    init_f.write(import_content)
        # break
