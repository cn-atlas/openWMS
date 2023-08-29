from celery import shared_task
from WMS.models.warehouse import WmsWarehouse
from WMS.models.check import WmsInventoryCheck


@shared_task
def check_inventory_monthly(*args, **kwargs):
    """
    每月定时生成盘库单，用作期初数
    """
    for warehouse in WmsWarehouse.objects.all():
        wic = WmsInventoryCheck(is_show=True,
                                inventory_check_type=0,
                                inventory_check_status=11,
                                warehouse=warehouse,
                                remark="期初自动盘点")
        wic.save()
