from import_export.fields import Field
from import_export.widgets import DateWidget


def get_all_verbose_info(model, fields, addon_header_dict=None) -> dict:
    # 额外字段别称
    if addon_header_dict is None: addon_header_dict = dict()

    # 模型字段别称
    model_field_names = {}
    for field in model._meta.fields:
        model_field_names[field.name] = model._meta.get_field(field.name).verbose_name

    # 在不改变原有 fields 顺序的前提下，替换默认字段表头文字
    _field_values = [model_field_names.get(field_name, None) if field_name in model_field_names and isinstance(
        model_field_names.get(field_name, None), str) else addon_header_dict.get(field_name, field_name) for field_name
                     in fields.keys()]

    headers = {k: v for k, v in zip(fields.keys(), _field_values)}
    return headers


class VerboseExportMixin:
    """Export with verbose name"""

    # 先注释掉，探究额外字段
    def get_export_headers(self):
        addon_header_dict = dict() if not hasattr(self.Meta, 'addon_header_dict') else self.Meta.addon_header_dict
        return get_all_verbose_info(self.Meta.model, self.fields, addon_header_dict).values()


class BaseMixin:
    pass
