from django.db import models
from utils.models.attachment import CommonFile


class SystemSettings(models.Model):
    '''
    系统信息, 显示在前端框架, 只查询 id=1 的记录
    '''
    site_name = models.CharField(blank=False, null=False, verbose_name="站点名称", default="openWMS", max_length=32)
    short_site_name = models.CharField(blank=True, null=True, verbose_name="名称简写", help_text="侧边栏收起的时候使用",
                                       default="WMS", max_length=16)
    copy_right_company_name = models.CharField(blank=True, null=True, verbose_name="版权旁边公司名称",
                                               default="CC", max_length=32)
    system_name = models.CharField(blank=True, null=True, verbose_name="版本旁边系统名称",
                                   default="openWMS", max_length=32)
    record = models.CharField(blank=True, null=True, verbose_name="备案信息", max_length=32)
    record_link = models.CharField(max_length=128, blank=True, null=True,
                                   default="https://beian.miit.gov.cn/#/Integrated/index", verbose_name="备案信息")
    version = models.CharField(blank=True, null=True, verbose_name="站点版本", default="Bata v0.0.1", max_length=32)
    other_info = models.CharField(blank=True, null=True, verbose_name="其他信息", max_length=32,
                                  help_text="比如地址等信息，放在网站脚部")
    small_logo = models.ForeignKey(CommonFile, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="small_logo_sysinfo",
                                   verbose_name="logo缩略图")
    big_logo = models.ForeignKey(CommonFile, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="big_logo_sysinfo",
                                 verbose_name="logo大图")
    other_icon = models.ForeignKey(CommonFile, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="other_icon",
                                   verbose_name="其他icon")

    def __str__(self):
        return f'{self.system_name}-{self.site_name}'

    class Meta:
        verbose_name = '系统信息'
        verbose_name_plural = '系统信息'
        ordering = ["id"]
