import os
import sys
import random
import django
from faker import Faker
from pathlib import Path
from django.apps import apps
from django.db import models

sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OpenWMS.settings")
django.setup()

fake = Faker(["zh-CN"])
# Step 1: Define the test case class template
test_case_template = """import logging
from django.test import TestCase
{import_content}


logger = logging.getLogger(__name__)

class {model}TestCase(TestCase):
    def setUp(self):
        logger.debug("Creating {model} object...")
        obj = {model}.objects.create({field_mapping})
        self.pk = obj.id
        self.assertEqual({model}.objects.count(), 1)

    def test_update_{model}(self):
        logger.debug("Updating {model} object...")
        update_data = {update_field_mapping}

        # Modify the fields you want to update
        {model}.objects.filter(pk=self.pk).update(**update_data)
        
        instance = {model}.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_{model}(self):
        logger.debug("Deleting {model} object...")
        self.assertEqual({model}.objects.count(), 1)
        # Delete the instance
        {model}.objects.filter(pk=self.pk).delete()
        self.assertEqual({model}.objects.count(), 0)

    # Add more test methods as needed
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


# from WMS.models.item import WmsAbsItem

# Step 2: Get a list of all Django models
# x_models = apps.get_models()
# x_models = [WmsAbsItem]
# Replace 'myapp' with the actual app label you want to get models for
# 如果直接使用 apps.get_models() 会包含系统默认 model 而这些 model 暂时不参与测试
app_labels = ['WMS']

# Get models for the specified app
for app_label in app_labels:
    app_models = apps.all_models[app_label]

    app = apps.get_app_config(app_label)
    app_directory_path = app.module.__path__[0]
    tests_dir = os.path.join(app_directory_path, "tests")

    # Step 3: Generate test cases for each model
    for _, model in app_models.items():
        # 注意⚠️：中文环境下适用，且注意自己写的表 verbose_name 包含"关系"字样的会跳过生成
        # 这一行为了排除 m2m 虚拟表生成测试，暂时不支持自动化为虚拟表生成测试用例
        if -1 != model._meta.verbose_name.find("关系"):
            # M2M 表暂时不测试
            # if not model._meta.many_to_many:
            model_name = model.__name__
            from django.db.models import Model

            field_mapping = []
            update_field_mapping = {}

            import_content = str(model)
            model_path = import_content.split("'")[1]
            from_path = '.'.join(model_path.split(".")[:len(model_path.split(".")) - 1])
            import_content = "from {} import {}".format(from_path, model_name)

            # Generate field mapping for each field
            for field in model._meta.fields:
                if field.name == "id":
                    continue
                field_type = field.get_internal_type()
                if isinstance(field, models.CharField) or isinstance(field, models.TextField) \
                        or isinstance(field, models.EmailField) or isinstance(field, models.DateField) \
                        or isinstance(field, models.DateTimeField):
                    field_mapping.append(f"{field.name}=\"{generate_random_data(field)}\"")
                else:
                    field_mapping.append(f"{field.name}={generate_random_data(field)}")
                #  时间格式还要转换，不参与测试, 外键、m2m 手动编写，不自动生成
                if not any([isinstance(field, models.DateTimeField),
                            isinstance(field, models.DateField),
                            isinstance(field, models.ForeignKey),
                            isinstance(field, models.ManyToManyField)]):
                    update_field_mapping[field.name] = generate_random_data(field)

            field_mapping = ', '.join(field_mapping)

            test_case = test_case_template.format(model=model_name, field_mapping=field_mapping,
                                                  update_field_mapping=update_field_mapping,
                                                  import_content=import_content)

            init_file_path = tests_dir + "/__init__.py"
            if not os.path.exists(tests_dir):
                os.mkdir(tests_dir)
                Path(init_file_path).touch()

            test_file_name = "{}/test_{}.py".format(tests_dir, model.__name__)
            if not os.path.exists(test_file_name):
                print("Generating {} file ...".format(test_file_name))
                with open(test_file_name, 'w+') as f:
                    f.write(test_case)
                with open(init_file_path, "r+") as init_f:
                    import_content = "from {}.tests import test_{}\n".format(app_label,
                                                                             model_name,
                                                                             model_name)
                    line_exists = False
                    for line in init_f.readlines():
                        if -1 != import_content.find(line):
                            line_exists = True
                    if not line_exists:
                        init_f.write(import_content)
