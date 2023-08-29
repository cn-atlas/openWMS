import logging
from django.test import TestCase
from WMS.models.inventory import WmsInventory
from WMS.models.item import WmsAbsItem, WmsItem
from WMS.models.warehouse import WmsRack, WmsArea, WmsWarehouse

logger = logging.getLogger(__name__)


class WmsInventoryTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsInventory object...")
        warehouse_obj = WmsWarehouse.objects.create(number="warehouse1", name="sdkfh")
        area_obj = WmsArea.objects.create(number="area12", name="area12", warehouse=warehouse_obj)
        rack_obj = WmsRack.objects.create(number="rack1", name="rack1", area=area_obj)
        abs_item_obj = WmsAbsItem.objects.create(number="abs_item1", name="abs_item1")
        item_obj = WmsItem.objects.create(abs_item=abs_item_obj, batch_number="number1")
        obj = WmsInventory.objects.create(is_show=True, create_time="2020-10-18 00:00:00",
                                          edit_time="2008-11-17 00:00:00", creator=None, editor=None, rack=rack_obj,
                                          item=item_obj, quantity=82.0, remark="论坛不同加入出来.")
        self.pk = obj.id
        self.assertEqual(WmsInventory.objects.count(), 1)

    def test_update_WmsInventory(self):
        logger.debug("Updating WmsInventory object...")
        update_data = {'is_show': True, 'creator': None, 'editor': None}

        # Modify the fields you want to update
        WmsInventory.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsInventory.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsInventory(self):
        logger.debug("Deleting WmsInventory object...")
        self.assertEqual(WmsInventory.objects.count(), 1)
        # Delete the instance
        WmsInventory.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsInventory.objects.count(), 0)

    # Add more test methods as needed
