from django.db import models
from django.contrib.auth.models import Group
from OpenWMS.base_model import BaseMPTTModel, BaseModel


class Company(BaseModel):
    """
    单位
    """
    number = models.CharField(max_length=50, default="", unique=True, verbose_name='单位编号')
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='单位名称', help_text="请填写全称")
    person = models.CharField(max_length=20, blank=True, null=True, verbose_name='联系人')
    address = models.CharField(max_length=100, blank=True, null=True, verbose_name='单位地址')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='单位电话')
    note = models.TextField(max_length=9999, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '单位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.number}-{self.name}'


class Department(BaseMPTTModel):
    """
    部门
    """
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL,
                                verbose_name="所属单位")
    department_number = models.CharField(max_length=128, null=True, blank=True, verbose_name="部门ID")
    department_name = models.CharField(max_length=128, null=True, blank=True, verbose_name="部门名称")
    group = models.ManyToManyField(Group, blank=True, verbose_name="分组", related_name="depart_groups",
                                   help_text="为了分组控制查询范围权限，跟user里面的group(user优先)同样生效")
    remark = models.CharField(max_length=128, null=True, blank=True, verbose_name="备注信息")

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.company}-{self.department_name}'
