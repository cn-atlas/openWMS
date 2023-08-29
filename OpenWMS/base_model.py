from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class BaseModel(models.Model):
    '''
    数据类的基类，提供数据公用的时间、创建人等信息
    '''
    is_show = models.BooleanField(default=False, verbose_name="是否显示", help_text="可用于控制删除")
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    edit_time = models.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")
    creator = models.ForeignKey('account.User', null=True, on_delete=models.SET_NULL, related_name="created_%(class)s",
                                verbose_name="创建人")
    editor = models.ForeignKey('account.User', null=True, blank=True, on_delete=models.SET_NULL,
                               related_name="edited_%(class)s",
                               verbose_name="修改人")

    class Meta:
        abstract = True


class BaseCheckModel(BaseModel):
    """
    需要审核的表来继承
    """
    is_checked = models.BooleanField(null=True, blank=True, verbose_name="是否审核")
    check_time = models.DateTimeField(blank=True, null=True, verbose_name="审核时间")
    check_user = models.ForeignKey('account.User', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="check_user_%(class)s", verbose_name="审核人")
    check_note = models.CharField(max_length=200, blank=True, null=True, verbose_name="审核备注")

    class Meta:
        abstract = True


class BaseMPTTModel(MPTTModel):
    '''
    数据类的基类，提供数据公用的时间、创建人等信息
    '''
    is_show = models.BooleanField(default=False, verbose_name="是否显示", help_text="可用于控制删除")
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name="创建时间")
    edit_time = models.DateTimeField(auto_now=True, null=True, verbose_name="修改时间")
    creator = models.ForeignKey('account.User', null=True, blank=True, on_delete=models.SET_NULL,
                                related_name="created_%(class)s", verbose_name="创建人")
    editor = models.ForeignKey('account.User', null=True, blank=True, on_delete=models.SET_NULL,
                               related_name="edited_%(class)s", verbose_name="修改人")
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='son_%(class)s',
                            verbose_name='上级')

    class Meta:
        abstract = True
