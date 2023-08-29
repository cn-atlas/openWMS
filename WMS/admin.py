from django.apps import apps
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.sessions.models import Session
from django.db.models.fields.files import FileField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.fields import CharField, TextField, EmailField
from OpenWMS.base_model import BaseModel
from auditlog.registry import auditlog
from django.contrib.admin.models import LogEntry
from django.conf import settings
from utils.models import SystemSettings
from account.models.user import User
from django.utils.translation import gettext_lazy
from django.contrib.auth.admin import UserAdmin


# from django_celery_results.models import TaskResult, GroupResult


def hide_item(modeladmin, request, queryset):
    # print(queryset)
    queryset.update(is_show=False)
    # messages.info(request, "更新任务已提交后台执行，请稍后刷新页面查看结果！")


def show_item(modeladmin, request, queryset):
    queryset.update(is_show=True)
    # messages.info(request, "更新任务已提交后台执行，请稍后刷新页面查看结果！")


hide_item.short_description = "设置为不可见"
show_item.short_description = "设置为可见"


class UserInfoAdmin(UserAdmin):
    list_per_page = settings.ADMIN_ITEM_NUM_PER_PAGE
    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
        (gettext_lazy('基础信息'), {'fields': ('username', 'nickname', 'first_name', 'mobile', 'email',
                                           'password')}),
        # (gettext_lazy('单位信息'),
        #  {'fields': ('gender', 'icon', 'company', 'title', 'birthday', 'description')}),
        # (gettext_lazy('部门信息'), {'fields': ('department', 'is_director')}),
        (gettext_lazy('账户权限'), {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups',
                                           'user_permissions')}),
        (gettext_lazy('重要日期'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('id', 'username', 'email', 'nickname', 'first_name', 'mobile')
    search_fields = [f.name for f in User._meta.fields if
                     isinstance(f, CharField) or isinstance(f, TextField) or isinstance(f, EmailField)]


# 特殊模型
except_models = [Session, User]
except_fields = [field.name for field in BaseModel._meta.fields if field.name not in ["id", "create_time"]]

model_list_fields = {
    # User: ["id", "username", "nickname", "email", "is_active", "is_staff"],
    # Sample: ["id", "is_show", "barcode", "name", "age", "creator"],
    # Customer: ["id", "number", "name", "company", "customer_type", "payment_type", "seller", "customer_service"],
}

addition_search_fields = {
    # ProductPrice: ["product__name", "product__number"],
    # ProductSellerPrice: ["price__product__name", "price__product__number"],
    # ProductCustomerPrice: ["price__product__name", "price__product__number"],
    # InternalSample: ["sample__barcode"],
    # OrderProduct: ["order__order_number"]
}


class ListAdminMixin:
    """
    # 统一处理后台显示和搜索，再也不怕后台搜索500了
    # https://medium.com/hackernoon/automatically-register-all-models-in-django-admin-django-tips-481382cf75e5
    # model._meta.fields 不包含 manytomany，要使用 model._meta.get_fields()  https://stackoverflow.com/a/43036789
    """

    def __init__(self, model, admin_site):
        x_except_fields = except_fields
        for field in model._meta.fields:
            if isinstance(field, TextField):
                x_except_fields = x_except_fields + [field.name]
        if model in model_list_fields:
            self.list_display = model_list_fields[model]
        else:
            self.list_display = [field.name for field in model._meta.fields if field.name not in x_except_fields]
        self.search_fields = [field.name for field in model._meta.fields if
                              isinstance(field, CharField) or isinstance(field, TextField)
                              or isinstance(field, EmailField) or isinstance(field, FileField)]
        if model in addition_search_fields:
            self.search_fields.extend(addition_search_fields[model])
        self.autocomplete_fields = [field.name for field in model._meta.fields if isinstance(field, ForeignKey)]
        self.list_select_related = [field.name for field in model._meta.fields if isinstance(field, ForeignKey)]
        self.filter_horizontal = [field.name for field in model._meta.get_fields() if
                                  isinstance(field, ManyToManyField)]
        self.list_per_page = settings.ADMIN_ITEM_NUM_PER_PAGE
        if hasattr(model, "is_show"):
            self.actions = [hide_item, show_item]
        # simple-admin  好像不支持这个属性
        # self.list_filter = []
        # if hasattr(model, "create_time"):
        #     self.list_filter += [('create_time', DateTimeRangeFilter)]
        super(ListAdminMixin, self).__init__(model, admin_site)


for model in apps.get_models():
    admin_class = type('AdminClass', (ListAdminMixin, ImportExportModelAdmin), {})
    try:
        if model not in except_models:
            admin.site.register(model, admin_class)
            if model not in [LogEntry]:
                auditlog.register(model)
    except admin.sites.AlreadyRegistered:
        pass

admin.site.register(User, UserInfoAdmin)

# 更改数据库的时候临时注释掉，这里是 admin 的站点信息，改完还要取消注释
try:
    system_settings = SystemSettings.objects.first()
    if system_settings:
        admin.site.site_title = system_settings.site_name
        admin.site.site_header = system_settings.short_site_name
except Exception as e:
    print(e)
