from OpenWMS.base_model import models, BaseModel, BaseMPTTModel


class WmsItemType(BaseMPTTModel):
    type_name = models.CharField(max_length=30, blank=True, null=True, verbose_name='物料类型名称')
    status = models.CharField(max_length=1, default="0", verbose_name='类型状态', help_text="0正常 1停用")

    def __str__(self):
        return f'{self.type_name}'

    class Meta:
        verbose_name = '物料类型'
        verbose_name_plural = verbose_name


class WmsAbsItem(BaseModel):
    number = models.CharField(max_length=20, verbose_name='编号')
    name = models.CharField(max_length=60, verbose_name='名称')
    specs = models.CharField(max_length=60, null=True, blank=True, verbose_name='规格')
    model = models.CharField(max_length=60, null=True, blank=True, verbose_name='型号')
    manufacturer = models.CharField(max_length=60, null=True, blank=True, verbose_name='厂商')
    item_type = models.ForeignKey(WmsItemType, null=True, blank=True, related_name="type_%(class)s",
                                  on_delete=models.SET_NULL, verbose_name="物料类型")
    unit = models.CharField(max_length=20, blank=True, null=True, verbose_name='计量单位')
    quantity = models.DecimalField(max_digits=20, decimal_places=2, default=10, verbose_name='安全库存')
    total_number = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name='库存总数',
                                       help_text="包含所有仓库库区货架的该类物料")
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return f'{self.number}-{self.name}'

    class Meta:
        verbose_name = '物料'
        verbose_name_plural = verbose_name


class WmsItem(BaseModel):
    """
    应该每批次都有新编号和记录，这样才有有效期
    物料编号，物料名称，规格，型号，单位，批号，有效期，备注
    """
    abs_item = models.ForeignKey(WmsAbsItem, null=True, blank=True, related_name="abs_item_%(class)s",
                                 on_delete=models.CASCADE,
                                 verbose_name='物料')
    batch_number = models.CharField(max_length=64, blank=True, null=True, verbose_name='批次号')
    produce_date = models.DateTimeField(blank=True, null=True, verbose_name='生产日期')
    expiry_date = models.DateTimeField(blank=True, null=True, verbose_name='有效期至')
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return f'{self.abs_item}-{self.batch_number}'

    class Meta:
        verbose_name = '批次物料'
        verbose_name_plural = verbose_name
