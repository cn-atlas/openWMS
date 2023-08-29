from django.db import models
from django.contrib.auth.models import AbstractUser
from .department import Company, Department
from tools.utils import get_date_time_now_local


class UserType(models.Model):
    name = models.CharField(max_length=16, verbose_name="名称")
    remark = models.CharField(max_length=128, null=True, blank=True, verbose_name="备注")

    class Meta:
        verbose_name_plural = '用户类别'
        verbose_name = '用户类别'

    def __str__(self):
        return f'{self.name}'


class User(AbstractUser):
    """
    用户信息表
    """
    user_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='用户代码', help_text='沿用样本系统编码')
    title = models.CharField(max_length=50, blank=True, verbose_name='标题')
    email = models.EmailField(null=True, blank=True)
    nickname = models.CharField(max_length=50, null=True, blank=True, verbose_name='昵称')
    mobile = models.CharField(max_length=32, null=True, blank=True, verbose_name='手机')
    description = models.TextField(max_length=10000, blank=True, null=True, verbose_name='个人简介')
    cls = models.ForeignKey(UserType, null=True, blank=True, related_name="class_users", on_delete=models.SET_NULL,
                            verbose_name='用户类别')
    gender = models.CharField(max_length=50, null=True, blank=True, verbose_name='性别')
    company = models.ForeignKey(Company, null=True, blank=True, related_name="company_users",
                                on_delete=models.SET_NULL, verbose_name='所属公司')
    department = models.ForeignKey(Department, null=True, blank=True, related_name="department_users",
                                   on_delete=models.SET_NULL, verbose_name='部门/分公司', help_text="内部员工专用")
    is_director = models.BooleanField(default=False, verbose_name="是否部门主管")
    position = models.CharField(max_length=128, null=True, blank=False, default='', verbose_name='职位信息')
    job_number = models.CharField(max_length=128, null=True, blank=False, default='', db_index=True,
                                  verbose_name='员工工号')
    create_time = models.DateTimeField(auto_now_add=get_date_time_now_local(), null=True, verbose_name="创建时间")
    modify_time = models.DateTimeField(auto_now=get_date_time_now_local(), null=True, verbose_name="修改时间")
    icon = models.ForeignKey("utils.UserIcon", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="用户头像")

    class Meta(AbstractUser.Meta):
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"

    def __str__(self):
        return f'{self.username}-{self.nickname}-{self.first_name}'


class ValidCode(models.Model):
    """
    验证码，包括邮件、短信验证码、重设密码
    验证码保留多条记录，在有限时间内都有效
    """
    credential = models.CharField(max_length=128, null=True, blank=True, verbose_name="用户凭证")
    valid_type = models.CharField(max_length=32, null=True, blank=True, verbose_name="验证类型")
    valid_code = models.CharField(max_length=32, null=True, blank=True, verbose_name="验证码")
    uuid = models.CharField(max_length=128, null=True, blank=True, verbose_name="UUID",
                            help_text="无特殊意义，用来标记唯一的验证码；和用于邮件验证链接")
    create_time = models.DateTimeField(auto_now_add=get_date_time_now_local(), null=True, verbose_name="创建时间")
    modify_time = models.DateTimeField(auto_now=get_date_time_now_local(), null=True, verbose_name="修改时间")

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.credential}-{self.valid_type}'


class LoginLog(models.Model):
    """
    用户登录日志
    """
    credential = models.CharField(max_length=128, null=True, blank=True, verbose_name="用户凭证")
    method = models.CharField(max_length=128, null=True, blank=True, verbose_name="登录方式 WEB OAuth")
    login_username = models.CharField(max_length=128, null=True, blank=True, verbose_name="登陆用户名")
    ip = models.CharField(max_length=128, null=True, blank=True, verbose_name="登录ip")
    city = models.CharField(max_length=128, null=True, blank=True, verbose_name="登陆城市")
    agent = models.TextField(null=True, blank=True, verbose_name="浏览器信息")
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name="备注，登录失败的原因")
    status = models.BooleanField(default=False, verbose_name="是否成功", help_text="成功为True")
    login_time = models.DateTimeField(auto_now_add=get_date_time_now_local(), null=True, verbose_name="登陆时间")

    class Meta:
        verbose_name_plural = '登录日志'
        verbose_name = '登录日志'

    def __str__(self):
        status = "登录成功" if self.status else "登录失败"
        return f'{self.credential}-{self.method}-{status}'
