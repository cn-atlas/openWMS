from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from WMS.models.inventory import WmsInventory
from WMS.signals.pre_save import get_current_user
from WMS.models.check import WmsInventoryCheck, WmsInventoryCheckDetail


@receiver(m2m_changed, sender=WmsInventoryCheck.item.through)
def inventory_item_created(sender, instance, action, pk_set, *args, **kwargs):
    if action == 'post_add':
        if instance.inventory_check_type == 3:
            inventories = WmsInventory.objects.filter(item__in=instance.item.all()).all()
            check_details = []
            request_user = get_current_user()
            for inventory in inventories:
                check_details.append(WmsInventoryCheckDetail(is_show=True, creator=request_user,
                                                             inventory_check=instance, rack=inventory.rack,
                                                             item=inventory.item, quantity=inventory.quantity))
            WmsInventoryCheckDetail.objects.bulk_create(check_details)
