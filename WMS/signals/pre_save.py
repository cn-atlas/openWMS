import uuid
from django.dispatch import receiver
from django.db.models.signals import pre_save
from tools.utils import logger
from OpenWMS.middleware import GetUserAnywhereMiddleware
from WMS.models.item import WmsAbsItem
from WMS.models.check import WmsInventoryCheck
from WMS.models.receipt import WmsReceiptOrder, WmsReceiptOrderDetail
from WMS.models.shipment import WmsShipmentOrder, WmsShipmentOrderDetail
from WMS.models.inventory import WmsInventory, WmsInventoryHistory
from WMS.models.movement import WmsInventoryMovement, WmsInventoryMovementDetail


def get_request():
    request = GetUserAnywhereMiddleware(get_response=None)
    try:
        request = request.thread_local.current_request
        return request
    except AttributeError:
        return None


def get_current_user():
    request = get_request()
    if request:
        return request.user
    return None


def inventory_in(item, rack, m_type, movement_obj, receipt_obj, shipment_obj, quantity, user):
    """
    调整库存并创建入库记录

    :param shipment_obj:
    :param item:
    :param rack:
    :param m_type:
    :param movement_obj:
    :param receipt_obj:
    :param quantity:
    :param user:
    :return:
    """
    try:
        ivt = WmsInventory.objects.filter(item=item, rack=rack, is_show=True).first()
        if not ivt:
            wi = WmsInventory(is_show=True, rack=rack, item=item, quantity=quantity, creator=user)
            wi.save()
            balance = quantity
        else:
            ivt.quantity += quantity
            balance = ivt.quantity
            ivt.save()
        if m_type == 3:
            inventory = {"inventory_movement": movement_obj, "remark": "入库"}
        elif m_type == 1:
            inventory = {"inventory_receipt_order": receipt_obj, "remark": "入库"}
        elif m_type == -2:
            inventory = {"inventory_shipment_order": shipment_obj, "remark": "取消出库"}
        elif m_type > 3:
            inventory = {"remark": "手动调整"}
        else:
            raise Exception("逻辑错误，请检查入库操作！")
        # 调整总库存
        abs_item = WmsAbsItem.objects.filter(id=item.abs_item.id, is_show=True).first()
        abs_item.total_number += quantity
        # 创建操作记录
        wih = WmsInventoryHistory(is_show=True, **inventory, form_type=m_type, item=item,
                                  number_type="+", rack=rack, quantity=quantity, balance=balance,
                                  creator=user)
        wih.save()
        return True
    except Exception as e:
        print(e)
    return False


def inventory_out(item, rack, m_type, movement_obj, receipt_obj, shipment_obj, quantity, user):
    """
    调整库存并创建出库记录

    :param receipt_obj:
    :param item:
    :param rack:
    :param m_type:
    :param movement_obj:
    :param shipment_obj:
    :param quantity:
    :param user:
    :return:
    """
    try:
        ivt = WmsInventory.objects.filter(item=item, rack=rack, is_show=True).first()
        ivt.quantity -= quantity
        balance = ivt.quantity
        ivt.save()
        if m_type == 3:
            inventory = {"inventory_movement": movement_obj, "remark": "移库出库"}
        elif m_type == 2:
            inventory = {"inventory_shipment_order": shipment_obj, "remark": "出库"}
        elif m_type == -1:
            inventory = {"inventory_receipt_order": receipt_obj, "remark": "取消入库"}
        elif m_type > 3:
            inventory = {"remark": "手动调整"}
        else:
            raise Exception("逻辑错误，请检查出库操作！")
        # 调整总库存
        abs_item = WmsAbsItem.objects.filter(id=item.abs_item.id, is_show=True).first()
        abs_item.total_number -= quantity
        wih = WmsInventoryHistory(is_show=True, **inventory, form_type=m_type, item=item,
                                  number_type="-", rack=rack, quantity=quantity, balance=balance,
                                  creator=user)
        wih.save()
        return True
    except Exception as e:
        logger.error(e)
    return False


def process_detail(instance, details):
    if instance.status > 1:
        # 判断是否是部分相等
        all_move = True
        for ob in details:
            if ob.plan_quantity > ob.real_quantity:
                ob.status = 2
                all_move = False
            else:
                ob.status = 3
            ob.save()
        # 前端控制 实际数量不大于计划数量
        if not all_move:
            instance.status = 2
        else:
            instance.status = 3
    else:
        for ob in details:
            ob.status = instance.status
            ob.save()


@receiver(pre_save, sender=WmsInventoryMovement)
def inventory_movement(sender, instance, **kwargs):
    """
    监听移库单，用来处理移库单 按计划移动或者部分移动的时候更改移库单详情表里面的状态
    # 可以直接算出来是不是 按计划出入库或者部分出入库

    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    old_instance = WmsInventoryMovement.objects.filter(id=instance.id, is_show=True).first()
    if old_instance:
        if old_instance.status != instance.status:
            movement_detail = WmsInventoryMovementDetail.objects.filter(inventory_movement=instance, is_show=True).all()
            process_detail(instance, movement_detail)


@receiver(pre_save, sender=WmsInventoryMovementDetail)
def inventory_movement_detail(sender, instance, **kwargs):
    """
    监听移库单详情

    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    user = get_current_user()
    old_instance = WmsInventoryMovementDetail.objects.filter(id=instance.id, is_show=True).first()
    if old_instance:
        if old_instance.status != instance.status:
            # 由移动还原
            if old_instance.status > 0 and instance.status < 1:
                inventory_in(item=instance.inventory.item, rack=instance.source_rack, m_type=3,
                             movement_obj=instance.inventory_movement, quantity=instance.real_quantity, user=user,
                             receipt_obj=None, shipment_obj=None)
                inventory_out(item=instance.inventory.item, rack=instance.target_rack, m_type=3,
                              movement_obj=instance.inventory_movement, quantity=instance.real_quantity, user=user,
                              shipment_obj=None, receipt_obj=None)
            # 审批通过，到待操作、部分操作或者操作完成
            if instance.status > 0 and old_instance.status < 1:
                inventory_out(item=instance.inventory.item, rack=instance.source_rack, m_type=3,
                              movement_obj=instance.inventory_movement, quantity=instance.real_quantity, user=user,
                              shipment_obj=None, receipt_obj=None)
                inventory_in(item=instance.inventory.item, rack=instance.target_rack, m_type=3,
                             movement_obj=instance.inventory_movement, quantity=instance.real_quantity, user=user,
                             receipt_obj=None, shipment_obj=None)


@receiver(pre_save, sender=WmsReceiptOrder)
def inventory_receipt(sender, instance, **kwargs):
    """
    # 可以直接算出来是不是 按计划出入库或者部分出入库

    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    old_instance = WmsReceiptOrder.objects.filter(id=instance.id, is_show=True).first()
    if old_instance:
        # 入库单
        if old_instance.status != instance.status:
            receipt_detail = WmsReceiptOrderDetail.objects.filter(receipt_order=instance, is_show=True).all()
            process_detail(instance, receipt_detail)


@receiver(pre_save, sender=WmsReceiptOrderDetail)
def inventory_receipt_detail(sender, instance, **kwargs):
    user = get_current_user()
    old_instance = WmsReceiptOrderDetail.objects.filter(id=instance.id, is_show=True).first()
    if old_instance:
        if old_instance.status != instance.status:
            # 退库
            if old_instance.status > 1 and instance.status < 2:
                inventory_out(item=instance.item, rack=instance.rack, m_type=-1,
                              movement_obj=None, quantity=instance.real_quantity, user=user,
                              receipt_obj=instance.receipt_order, shipment_obj=None)
            # 到部分入库或者入库完成
            if instance.status > 1 and old_instance.status < 2:
                inventory_in(item=instance.item, rack=instance.rack, m_type=1,
                             movement_obj=None, quantity=instance.real_quantity, user=user,
                             receipt_obj=instance.receipt_order, shipment_obj=None)


@receiver(pre_save, sender=WmsShipmentOrder)
def inventory_shipment(sender, instance, **kwargs):
    """
    # 可以直接算出来是不是 按计划出入库或者部分出入库

    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    old_instance = WmsShipmentOrder.objects.filter(id=instance.id, is_show=True).first()
    if old_instance:
        # 移动状态变更
        if old_instance.status != instance.status:
            shipment_detail = WmsShipmentOrderDetail.objects.filter(shipment_order=instance, is_show=True).all()
            # 每条循环判断是否按计划入库或者部分入库
            process_detail(instance, shipment_detail)


@receiver(pre_save, sender=WmsShipmentOrderDetail)
def inventory_shipment_detail(sender, instance, **kwargs):
    user = get_current_user()
    old_instance = WmsShipmentOrderDetail.objects.filter(id=instance.id, is_show=True).first()
    if old_instance:
        # TODO: 如果硬删除，在 >1 的状态库存也要调整回来
        if old_instance.status != instance.status:
            # 取消出库
            if old_instance.status > 0 and instance.status < 1:
                inventory_in(item=instance.inventory.item, rack=instance.rack, m_type=-2,
                             movement_obj=None, quantity=instance.real_quantity, user=user,
                             receipt_obj=None, shipment_obj=instance.shipment_order)
            # 现：审批完成之后就减库存 原：到部分出库或者出库完成
            if instance.status > 0 and old_instance.status < 1:
                inventory_out(item=instance.inventory.item, rack=instance.rack, m_type=2,
                              movement_obj=None, quantity=instance.real_quantity, user=user,
                              receipt_obj=None, shipment_obj=instance.shipment_order)


@receiver(pre_save, sender=WmsShipmentOrder)
@receiver(pre_save, sender=WmsReceiptOrder)
@receiver(pre_save, sender=WmsInventoryMovement)
@receiver(pre_save, sender=WmsInventoryCheck)
def generate_number(sender, instance, **kwargs):
    old_instance = sender.objects.filter(id=instance.id, is_show=True).first()
    if not old_instance:
        if not instance.number:
            instance.number = str(uuid.uuid4())
    # 出库、移库审核，暂时不要审核步骤，如果需要增加审核步骤，请把下面代放出来即可
    # if sender in [WmsShipmentOrder, WmsInventoryMovement]:
    #     if old_instance:
    #         # 审核变化并通过之后由待审核变为待出库
    #         if old_instance.is_checked != instance.is_checked and instance.is_checked:
    #             instance.status = 1
    #             # 更新, 没有信号
    #             if sender == WmsShipmentOrder:
    #                 WmsShipmentOrderDetail.objects.filter(shipment_order=instance).update(status=1)
    #             if sender == WmsInventoryMovement:
    #                 WmsInventoryMovementDetail.objects.filter(inventory_movement=instance).update(status=1)


@receiver(pre_save, sender=WmsInventoryCheck)
def inventory_check(sender, instance, **kwargs):
    old_instance = sender.objects.filter(id=instance.id, is_show=True).first()
    if old_instance:
        if old_instance.is_checked != instance.is_checked:
            if instance.is_checked:
                instance.inventory_check_status = "22"
                # 计算盈亏
                inventory_check_total = 0
                try:
                    for detail in instance.inventory_check_wmsinventorycheckdetail.all():
                        inventory_check_total += abs(detail.quantity - detail.check_quantity)
                    instance.inventory_check_total = inventory_check_total
                except TypeError as e:
                    logger.error("盘点详情缺失数据: ", e)
                    if instance(instance.remark, str):
                        instance.remark += "\n盈亏计算失败(数据缺失)"
                    else:
                        instance.remark = "盈亏计算失败(数据缺失)"
            else:
                instance.inventory_check_status = "11"
                instance.inventory_check_total = 0
