import logging
from django.test import TestCase
from WMS.models.inventory import WmsInventoryHistory
from WMS.models.item import WmsAbsItem, WmsItem
from WMS.models.warehouse import WmsRack, WmsArea, WmsWarehouse

logger = logging.getLogger(__name__)


class WmsInventoryHistoryTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsInventoryHistory object...")
        warehouse_obj = WmsWarehouse.objects.create(number="warehouse1", name="sdkfh")
        area_obj = WmsArea.objects.create(number="area12", name="area12", warehouse=warehouse_obj)
        rack_obj = WmsRack.objects.create(number="rack1", name="rack1", area=area_obj)
        abs_item_obj = WmsAbsItem.objects.create(number="abs_item1", name="abs_item1")
        item_obj = WmsItem.objects.create(abs_item=abs_item_obj, batch_number="number1")
        obj = WmsInventoryHistory.objects.create(is_show=False, create_time="1992-08-15 00:00:00",
                                                 edit_time="2016-05-22 00:00:00", creator=None, editor=None,
                                                 inventory_movement=None, inventory_receipt_order=None,
                                                 inventory_shipment_order=None, form_type=19, number_type="1",
                                                 item=item_obj, rack=rack_obj, quantity=71.0, balance=49.0,
                                                 remark="设备方式内容时间方面.")
        self.pk = obj.id
        self.assertEqual(WmsInventoryHistory.objects.count(), 1)

    def test_update_WmsInventoryHistory(self):
        logger.debug("Updating WmsInventoryHistory object...")
        update_data = {'creator': None, 'editor': None, 'quantity': 70.0, 'balance': 33.0}

        # Modify the fields you want to update
        WmsInventoryHistory.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsInventoryHistory.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsInventoryHistory(self):
        logger.debug("Deleting WmsInventoryHistory object...")
        self.assertEqual(WmsInventoryHistory.objects.count(), 1)
        # Delete the instance
        WmsInventoryHistory.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsInventoryHistory.objects.count(), 0)

    # Add more test methods as needed
