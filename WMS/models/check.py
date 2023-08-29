from OpenWMS.base_model import models, BaseModel, BaseCheckModel
from WMS.models.item import WmsItem
from WMS.models.warehouse import WmsRack, WmsWarehouse, WmsArea
from utils.models.attachment import InventoryFile


class WmsInventoryCheck(BaseCheckModel):
    number = models.CharField(max_length=64, default="", verbose_name='盘点单号', help_text="系统自动生成")
    inventory_check_type = models.IntegerField(blank=True, null=True, verbose_name='盘点类型',
                                               help_text="0：仓库盘点，1: 库区盘点，2：货架盘点, 3: 物料盘点")
    inventory_check_status = models.IntegerField(default="11", verbose_name='盘点单状态', help_text='11：盘点中 22：已完成')
    inventory_check_total = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name='总盈亏数')
    warehouse = models.ForeignKey(WmsWarehouse, related_name="warehouse_%(class)s", on_delete=models.CASCADE,
                                  null=True, blank=True, verbose_name='盘点仓库', help_text="仓库、库区、货架三选一")
    area = models.ForeignKey(WmsArea, related_name="area_%(class)s", on_delete=models.CASCADE, verbose_name='盘点库区',
                             null=True, blank=True, help_text="仓库、库区、货架四选一")
    rack = models.ForeignKey(WmsRack, related_name="rack_%(class)s", on_delete=models.CASCADE, verbose_name='盘点货架',
                             null=True, blank=True, help_text="仓库、库区、货架四选一")
    item = models.ManyToManyField(WmsItem, related_name="item_%(class)s", verbose_name='物料',
                                  blank=True, help_text="仓库、库区、货架四选一")
    attachment = models.ForeignKey(InventoryFile, blank=True, null=True, related_name="attachment_%(class)s",
                                   on_delete=models.SET_NULL, verbose_name='附件文件')
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '盘库单'
        verbose_name_plural = verbose_name


class WmsInventoryCheckDetail(BaseModel):
    inventory_check = models.ForeignKey(WmsInventoryCheck, related_name="inventory_check_%(class)s",
                                        on_delete=models.CASCADE, verbose_name='库存盘点单')
    rack = models.ForeignKey(WmsRack, related_name="rack_%(class)s", on_delete=models.CASCADE, verbose_name='货架')
    item = models.ForeignKey(WmsItem, related_name="item_%(class)s", on_delete=models.CASCADE, verbose_name='物料')
    quantity = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='账面库存')
    check_quantity = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='实际库存')
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '盘库单详情'
        verbose_name_plural = verbose_name
