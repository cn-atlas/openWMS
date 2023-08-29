from django.apps import apps
from django.contrib.auth.models import User, Group, Permission
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry, ContentType

all_models = apps.get_models()

# dict 填写规范 {<model object>: <filter object>}
# 不生成 Filter
except_models = {
    Session,
    # User,
    LogEntry,
    # Group,
    Permission,
    ContentType
}


def get_import_line(x_model):
    model_str = str(x_model)
    x_model_path = model_str.split("'")[1]
    x_from_path = '.'.join(x_model_path.split(".")[:len(x_model_path.split(".")) - 1])
    return "from {} import {}".format(x_from_path, x_model.__name__)
