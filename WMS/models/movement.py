from OpenWMS.base_model import models, BaseModel, BaseCheckModel
from WMS.models.warehouse import WmsRack


class WmsInventoryMovement(BaseCheckModel):
    number = models.CharField(max_length=64, default="", verbose_name='编号')
    source_rack = models.ForeignKey(WmsRack, null=True, blank=True, related_name="source_rack_%(class)s",
                                    on_delete=models.CASCADE, verbose_name='源货架', help_text="如果没有来源货架移库，请写备注")
    target_rack = models.ForeignKey(WmsRack, null=True, blank=True, related_name="target_rack_%(class)s",
                                    on_delete=models.CASCADE, verbose_name='目标货架', help_text="如果没有目标货架移库，请写备注")
    status = models.IntegerField(default=0, verbose_name='状态',
                                 help_text="-2：取消移动， -1：审核拒绝，0: 移库审批中，1：待移动，2：部分移动，3：按计划移动")
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '移库单'
        verbose_name_plural = verbose_name


class WmsInventoryMovementDetail(BaseModel):
    inventory_movement = models.ForeignKey(WmsInventoryMovement, related_name="movement_%(class)s",
                                           on_delete=models.CASCADE, verbose_name='移库单')
    # item = models.ForeignKey(WmsItem, related_name="item_%(class)s", on_delete=models.CASCADE, verbose_name='物料')
    inventory = models.ForeignKey('WMS.WmsInventory', related_name="inventory_%(class)s", on_delete=models.CASCADE,
                                  null=True, blank=True, verbose_name='库存', help_text="库存为了方便加减的时候控制数量")
    plan_quantity = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name='计划数量')
    real_quantity = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name='实际数量')
    source_rack = models.ForeignKey(WmsRack, related_name="source_rack_%(class)s", on_delete=models.CASCADE,
                                    verbose_name='源货架')
    target_rack = models.ForeignKey(WmsRack, related_name="target_rack_%(class)s", on_delete=models.CASCADE,
                                    verbose_name='目标货架')
    status = models.IntegerField(default=0, verbose_name='状态',
                                 help_text="-2：取消移动， -1：审核拒绝，0: 移库审批中，1：待移动，2：部分移动，3：按计划移动")
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '库存移动详情'
        verbose_name_plural = verbose_name
