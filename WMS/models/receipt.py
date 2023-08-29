from OpenWMS.base_model import models, BaseModel
from WMS.models.item import WmsItem
from WMS.models.warehouse import WmsRack


class WmsSupplier(BaseModel):
    number = models.CharField(max_length=20, verbose_name='编号')
    name = models.CharField(max_length=60, verbose_name='企业抬头')
    bank_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='开户行')
    bank_account = models.CharField(max_length=40, blank=True, null=True, verbose_name='银行账户')
    address = models.CharField(max_length=80, blank=True, null=True, verbose_name='地址')
    mobile_no = models.CharField(max_length=13, blank=True, null=True, verbose_name='手机号')
    tel_no = models.CharField(max_length=13, blank=True, null=True, verbose_name='座机号')
    contact = models.CharField(max_length=30, blank=True, null=True, verbose_name='联系人')
    level = models.CharField(max_length=10, blank=True, null=True, verbose_name='级别')
    email = models.CharField(max_length=50, blank=True, null=True, verbose_name='Email')
    item = models.ManyToManyField(WmsItem, related_name="item_%(class)s", blank=True, verbose_name='供应物料')
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '供应商'
        verbose_name_plural = verbose_name


class WmsReceiptOrder(BaseModel):
    number = models.CharField(max_length=64, default="", verbose_name='入库单号')
    receipt_type = models.IntegerField(blank=True, null=True, verbose_name='入库类型', help_text="0 采购, 1 调库, 2 其他入库")
    supplier = models.ForeignKey(WmsSupplier, related_name="supplier_%(class)s", on_delete=models.SET_NULL, null=True,
                                 blank=True, verbose_name='供应商')
    order_no = models.CharField(max_length=32, blank=True, null=True, verbose_name='订单号')
    payable_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='订单金额')
    status = models.IntegerField(default=1, verbose_name='入库状态',
                                 help_text="-2: 取消入库，1: 待入库, 2:部分入库，3:按计划入库")
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return f'{self.number}'

    class Meta:
        verbose_name = '入库单'
        verbose_name_plural = verbose_name


class WmsReceiptOrderDetail(BaseModel):
    receipt_order = models.ForeignKey(WmsReceiptOrder, null=True, blank=True, related_name="receipt_order_%(class)s",
                                      on_delete=models.SET_NULL, verbose_name='入库单')
    item = models.ForeignKey(WmsItem, related_name="item_%(class)s", on_delete=models.CASCADE, verbose_name='物料')
    plan_quantity = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='计划数量')
    real_quantity = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='实际数量')
    rack = models.ForeignKey(WmsRack, related_name="rack_%(class)s", on_delete=models.CASCADE, verbose_name='所属货架')
    money = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='金额')
    status = models.IntegerField(default=1, verbose_name='入库状态',
                                 help_text="-2: 取消入库，1: 待入库, 2:部分入库，3:按计划入库")
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return f'{self.receipt_order}-{self.item}'

    class Meta:
        verbose_name = '入库单详情'
        verbose_name_plural = verbose_name
