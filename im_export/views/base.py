import uuid
from drf_yasg import openapi
from tools.utils import get_date_time_now_local
from django_filters import rest_framework as filters


def field_to_openapi_type(field):
    if isinstance(field, filters.CharFilter):
        return openapi.TYPE_STRING
    elif isinstance(field, filters.NumberFilter):
        return openapi.TYPE_NUMBER
    # Add more cases for other filter types as needed
    else:
        return openapi.TYPE_STRING  # Default to string if the type is not recognized


def get_export_file_name(cls, request, f_type: str = "csv"):
    f_type = f_type.split(".")[-1]
    assert f_type in ["csv", "xls", "xlsx"], "文件类型错误"
    _file_name = None
    _query_params = dict(request.query_params)
    if 'f_name' in _query_params:
        __file_name = _query_params.pop("f_name")
        if isinstance(__file_name, str):
            if __file_name.endswith(f_type):
                _file_name = __file_name
            else:
                _file_name = __file_name + ".{}".format(f_type)
    if not _file_name:
        _file_name = f'export-{cls.Meta.model.__name__.lower()}-{get_date_time_now_local().strftime("%Y%m%d-%H%M%S")}-{str(uuid.uuid4()).split("-")[0]}.{f_type}'
    return _file_name
