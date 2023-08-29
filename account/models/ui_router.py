from django.db import models
from django.contrib.auth.models import Permission
from OpenWMS.base_model import BaseMPTTModel


class UIRouter(BaseMPTTModel):
    """
    前端路由权限
    """
    name = models.CharField(max_length=128, null=True, blank=True, verbose_name="路由名称")
    code = models.CharField(max_length=64, null=True, blank=True, verbose_name="路由代码")
    path = models.CharField(max_length=128, null=True, blank=True, verbose_name="路由path")
    icon = models.CharField(max_length=64, null=True, blank=True, verbose_name="路由图标代码")
    x_authority = models.ManyToManyField(Permission, blank=True, verbose_name="路由准入权限",
                                         help_text="只选择view 即可，前端控制也只用view。写的越少可见的人越多，为空是所有人都可见")
    component = models.CharField(max_length=128, null=True, blank=True, verbose_name="组件")
    redirect = models.CharField(max_length=512, null=True, blank=True, verbose_name="重定向地址")
    target = models.CharField(max_length=32, null=True, blank=True, verbose_name="跳转方式")
    hide_in_menu = models.BooleanField(default=False, verbose_name="在菜单中隐藏")
    hide_children_in_menu = models.BooleanField(default=False, verbose_name="隐藏子菜单")
    hide_breadcrumb = models.BooleanField(default=False, verbose_name="在面包屑导航中隐藏")
    priority = models.IntegerField(default=0, verbose_name="排序优先级", help_text="大数排在前面，支持负数,请跳跃编号，方便中间插入")
    remark = models.CharField(max_length=128, null=True, blank=True, verbose_name="备注信息")

    class Meta:
        ordering = ["-priority"]
        verbose_name_plural = '界面路由'
        verbose_name = '界面路由'

    def __str__(self):
        return f'{self.name}-{self.code}'
