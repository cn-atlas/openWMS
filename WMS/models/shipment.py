from account.models import User
from OpenWMS.base_model import models, BaseModel, BaseCheckModel
from WMS.models.warehouse import WmsRack


class WmsShipmentOrder(BaseCheckModel):
    """
    既是申请单又是出库单， shipment_order_type 1、物料申请单 2、出库单
    """
    number = models.CharField(max_length=64, default="", verbose_name='出库单号，系统自动生成')
    shipment_order_type = models.IntegerField(default=1, verbose_name='出库类型', help_text="1、物料申请单 2、出库单")
    order_no = models.CharField(max_length=50, blank=True, null=True, verbose_name='出库订单')
    to_customer = models.CharField(max_length=50, blank=True, null=True, verbose_name='外部领用人')
    to_user = models.ForeignKey(User, null=True, blank=True, related_name="user_%(class)s", on_delete=models.SET_NULL,
                                verbose_name="内部领用人")
    receivable_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='订单金额')
    status = models.IntegerField(default=0, verbose_name='出库单状态',
                                 help_text="-2：取消出库，-1: 审批拒绝，0: 出库审批中, 1: 待出库, 2: 部分出库， 3: 按计划出库")
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    @staticmethod
    def get_order_about_me_query_filter():
        # 只有加上本方法才支持权限范围查询（order除外，代码在filter_object_range里面）
        return True

    class Meta:
        verbose_name = '出库单'
        verbose_name_plural = verbose_name


class WmsShipmentOrderDetail(BaseModel):
    shipment_order = models.ForeignKey(WmsShipmentOrder, null=True, related_name="shipment_order_%(class)s",
                                       on_delete=models.SET_NULL, verbose_name='出库单')
    # item = models.ForeignKey(WmsItem, related_name="item_%(class)s", on_delete=models.CASCADE, verbose_name='物料')
    inventory = models.ForeignKey('WMS.WmsInventory', null=True, blank=True, related_name="inventory_%(class)s",
                                  on_delete=models.CASCADE, verbose_name='库存', help_text="库存为了方便加减的时候控制数量")
    plan_quantity = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='计划数量')
    real_quantity = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name='实际数量')
    rack = models.ForeignKey(WmsRack, related_name="rack_%(class)s", on_delete=models.CASCADE, verbose_name='所属货架')
    money = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='金额')
    status = models.IntegerField(default=0, verbose_name='出库状态',
                                 help_text="-2：取消出库，-1: 审批拒绝，0: 出库审批中, 1: 待出库, 2: 部分出库， 3: 按计划出库")
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    @staticmethod
    def get_order_about_me_query_filter():
        # 只有加上本方法才支持权限范围查询（order除外，代码在filter_object_range里面）
        return True

    class Meta:
        verbose_name = '出库单详情'
        verbose_name_plural = verbose_name


class WmsDelivery(BaseModel):
    shipment_order = models.ForeignKey(WmsShipmentOrder, null=True, blank=True, related_name="shipment_order_%(class)s",
                                       on_delete=models.SET_NULL, verbose_name='出库单')
    carrier = models.CharField(max_length=50, blank=True, null=True, verbose_name='承运商Id')
    delivery_date = models.DateTimeField(blank=True, null=True, verbose_name='发货日期')
    tracking_no = models.CharField(max_length=50, blank=True, null=True, verbose_name='快递单号')
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '发货记录'
        verbose_name_plural = verbose_name
