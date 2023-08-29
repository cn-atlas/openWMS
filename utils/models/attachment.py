from django.db import models
from datetime import datetime
from OpenWMS.base_model import BaseModel
from tools.utils import validate_file_extension


class AbstractCommonFiles(BaseModel):
    '''
    通用文件类，自动为每一个文件生成 uuid，可用于区分是否为同一批次文件
    不再使用单独一个表来保存所有图片路径，而是建一个抽象类，从抽象类继承生成其他表
    '''
    name = models.CharField(max_length=128, null=True, blank=True, verbose_name="名称")
    uuid = models.CharField(max_length=64, null=True, blank=True, verbose_name="uuid")
    type = models.CharField(max_length=255, null=True, blank=True, verbose_name="文件类型")
    remark = models.CharField(max_length=128, null=True, blank=True, verbose_name="备注")

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}-{self.remark}'


class UserIcon(AbstractCommonFiles):
    file = models.FileField(verbose_name="文件",
                            upload_to='uploads/user_icon/{}/{}'.format(datetime.today().year, datetime.today().month),
                            validators=[validate_file_extension])

    class Meta(AbstractCommonFiles.Meta):
        verbose_name = "用户头像"
        verbose_name_plural = verbose_name


class CommonFile(AbstractCommonFiles):
    file = models.FileField(verbose_name="文件",
                            upload_to='uploads/common_files/{}/{}'.format(datetime.today().year,
                                                                          datetime.today().month),
                            validators=[validate_file_extension])

    class Meta(AbstractCommonFiles.Meta):
        verbose_name = "其他文件"
        verbose_name_plural = verbose_name


class InventoryFile(AbstractCommonFiles):
    file = models.FileField(verbose_name="盘库单附件",
                            upload_to='uploads/inventory_files/{}/{}'.format(datetime.today().year,
                                                                             datetime.today().month),
                            validators=[validate_file_extension])

    class Meta(AbstractCommonFiles.Meta):
        verbose_name = "盘库单附件"
        verbose_name_plural = verbose_name
