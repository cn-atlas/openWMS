from OpenWMS.base_model import models, BaseModel
from WMS.models.item import WmsItem
from WMS.models.warehouse import WmsRack
from account.models.user import User


class WmsInventory(BaseModel):
    """
    关系变动信号如下：
        移库单 移动完成或者部分移动的时候，把移库单详情里面数量减去；同时插入库存变更记录
        入库单 按计划入库和部分入库的时候，把入库单详情里面数量加上，同时插入库存变更记录
        出库单 按计划出库和部分出库的时候，把移库单详情里面数量减去；同时插入库存变更记录
    """
    rack = models.ForeignKey(WmsRack, related_name="rack_%(class)s", on_delete=models.CASCADE, verbose_name='货架')
    item = models.ForeignKey(WmsItem, related_name="item_%(class)s", on_delete=models.CASCADE, verbose_name='物料')
    quantity = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name='库存')
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    class Meta:
        # 每个货架对应物料不允许有多条记录
        unique_together = ('rack', 'item')
        verbose_name = '当前库存'
        verbose_name_plural = verbose_name


class WmsInventoryHistory(BaseModel):
    inventory_movement = models.ForeignKey("WMS.WmsInventoryMovement", null=True, blank=True,
                                           related_name="movement_%(class)s", on_delete=models.CASCADE,
                                           verbose_name="移库单", help_text="移库单、入库单、出库单三选一")
    inventory_receipt_order = models.ForeignKey('WMS.WmsReceiptOrder', null=True, blank=True,
                                                related_name="receipt_order_%(class)s", on_delete=models.CASCADE,
                                                verbose_name="入库单", help_text="移库单、入库单、出库单三选一")
    inventory_shipment_order = models.ForeignKey('WMS.WmsShipmentOrder', null=True, blank=True,
                                                 related_name="shipment_order_%(class)s", on_delete=models.CASCADE,
                                                 verbose_name="出库单", help_text="移库单、入库单、出库单三选一")
    operator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="my_%(class)s", verbose_name="操作人")
    form_type = models.IntegerField(blank=True, null=True, verbose_name='操作类型',
                                    help_text=" -2： 取消出库，-1: 取消入库，1:入库, 2 出库, 3: 移库, 4: 手动调整, 5:过期丢弃, 6: 其他")
    number_type = models.CharField(max_length=8, null=True, blank=True, verbose_name='盈亏',
                                   help_text="入库 +， 出库 -, 移库要一对")
    item = models.ForeignKey(WmsItem, related_name="item_%(class)s", on_delete=models.CASCADE, verbose_name='物料')
    rack = models.ForeignKey(WmsRack, related_name="rack_%(class)s", on_delete=models.CASCADE, verbose_name='货架')
    quantity = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='库存变化')
    balance = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='当期余额')
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '库存变动记录'
        verbose_name_plural = verbose_name
