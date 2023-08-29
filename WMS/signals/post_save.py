from django.db.models.signals import post_save
from django.dispatch import receiver
from WMS.models.inventory import WmsInventory
from WMS.signals.pre_save import get_current_user
from WMS.models.check import WmsInventoryCheck, WmsInventoryCheckDetail


@receiver(post_save, sender=WmsInventoryCheck)
def generate_check_details(sender, instance, created, **kwargs):
    """
    创建完盘库单，自动绑定库存详情
    """
    if created:
        """
        item 属于 M2M 在 M2M_changed 里面
        """
        if instance.inventory_check_type == 0:
            inventories = WmsInventory.objects.filter(rack__area__warehouse=instance.warehouse).all()
        elif instance.inventory_check_type == 1:
            inventories = WmsInventory.objects.filter(rack__area=instance.area).all()
        elif instance.inventory_check_type == 2:
            inventories = WmsInventory.objects.filter(rack=instance.rack).all()
        else:
            inventories = []
        inventory_details = []
        request_user = get_current_user()
        for inventory in inventories:
            inventory_details.append(WmsInventoryCheckDetail(is_show=True, creator=request_user,
                                                             inventory_check=instance, rack=inventory.rack,
                                                             item=inventory.item, quantity=inventory.quantity))
        WmsInventoryCheckDetail.objects.bulk_create(inventory_details)
