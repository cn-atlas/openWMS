import logging
from django.test import TestCase
from WMS.models.check import WmsInventoryCheck, WmsInventoryCheckDetail
from WMS.models.item import WmsAbsItem, WmsItem
from WMS.models.warehouse import WmsRack, WmsArea, WmsWarehouse

logger = logging.getLogger(__name__)


class WmsInventoryCheckDetailTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsInventoryCheckDetail object...")
        warehouse_obj = WmsWarehouse.objects.create(number="warehouse1", name="sdkfh")
        area_obj = WmsArea.objects.create(number="area12", name="area12", warehouse=warehouse_obj)
        rack_obj = WmsRack.objects.create(number="rack1", name="rack1", area=area_obj)
        abs_item_obj = WmsAbsItem.objects.create(number="abs_item1", name="abs_item1")
        item_obj = WmsItem.objects.create(abs_item=abs_item_obj, batch_number="number1")
        check_obj = WmsInventoryCheck.objects.create(number="sdfjslfj")
        obj = WmsInventoryCheckDetail.objects.create(is_show=True, create_time="1963-10-09 00:00:00",
                                                     edit_time="1979-03-12 00:00:00", creator=None, editor=None,
                                                     inventory_check=check_obj, rack=rack_obj, item=item_obj,
                                                     quantity=98.0,
                                                     check_quantity=67.0, remark="经济认为得到的人这些是一.")
        self.pk = obj.id
        self.assertEqual(WmsInventoryCheckDetail.objects.count(), 1)

    def test_update_WmsInventoryCheckDetail(self):
        logger.debug("Updating WmsInventoryCheckDetail object...")
        update_data = {'remark': '如此拥有设备新闻客户.'}

        # Modify the fields you want to update
        WmsInventoryCheckDetail.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsInventoryCheckDetail.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsInventoryCheckDetail(self):
        logger.debug("Deleting WmsInventoryCheckDetail object...")
        self.assertEqual(WmsInventoryCheckDetail.objects.count(), 1)
        # Delete the instance
        WmsInventoryCheckDetail.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsInventoryCheckDetail.objects.count(), 0)

    # Add more test methods as needed
