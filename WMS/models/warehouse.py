from utils.models import models, BaseModel


class WmsWarehouse(BaseModel):
    number = models.CharField(max_length=20, verbose_name='编号')
    name = models.CharField(max_length=50, verbose_name='名称')
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return f'{self.number}-{self.name}'

    class Meta:
        verbose_name = "仓库"
        verbose_name_plural = verbose_name


class WmsArea(BaseModel):
    number = models.CharField(max_length=20, verbose_name='编号')
    name = models.CharField(max_length=60, verbose_name='名称')
    warehouse = models.ForeignKey(WmsWarehouse, related_name="ware_house_%(class)s", on_delete=models.CASCADE,
                                  verbose_name="所属仓库")
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return f'{self.number}-{self.name}'

    class Meta:
        verbose_name = "库区"
        verbose_name_plural = verbose_name


class WmsRack(BaseModel):
    warehouse = models.ForeignKey(WmsWarehouse, null=True, blank=True, related_name="ware_house_%(class)s",
                                  on_delete=models.CASCADE,
                                  verbose_name="所属仓库", help_text="辅助显示，自动填充禁止写入或通过此项查询")
    area = models.ForeignKey(WmsArea, related_name="area_%(class)s", on_delete=models.CASCADE,
                             verbose_name="所属库区")
    number = models.CharField(max_length=20, verbose_name='编号')
    name = models.CharField(max_length=60, blank=True, null=True, verbose_name='名称')
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return f'{self.number}-{self.name}'

    class Meta:
        verbose_name = "货架"
        verbose_name_plural = verbose_name
