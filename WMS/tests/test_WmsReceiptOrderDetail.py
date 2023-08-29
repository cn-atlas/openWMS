import logging
from django.test import TestCase
from WMS.models.item import WmsAbsItem, WmsItem
from WMS.models.warehouse import WmsRack, WmsArea, WmsWarehouse
from WMS.models.receipt import WmsReceiptOrderDetail

logger = logging.getLogger(__name__)


class WmsReceiptOrderDetailTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsReceiptOrderDetail object...")
        warehouse_obj = WmsWarehouse.objects.create(number="warehouse1", name="sdkfh")
        area_obj = WmsArea.objects.create(number="area12", name="area12", warehouse=warehouse_obj)
        rack_obj = WmsRack.objects.create(number="rack1", name="rack1", area=area_obj)
        abs_item_obj = WmsAbsItem.objects.create(number="abs_item1", name="abs_item1")
        item_obj = WmsItem.objects.create(abs_item=abs_item_obj, batch_number="number1")
        obj = WmsReceiptOrderDetail.objects.create(is_show=True, create_time="1908-08-08 00:00:00",
                                                   edit_time="1938-02-09 00:00:00", creator=None, editor=None,
                                                   receipt_order=None, item=item_obj, plan_quantity=61.0,
                                                   real_quantity=26.0, rack=rack_obj, money=79.0, status=14,
                                                   remark="应用觉得通过经济人员价格.")
        self.pk = obj.id
        self.assertEqual(WmsReceiptOrderDetail.objects.count(), 1)

    def test_update_WmsReceiptOrderDetail(self):
        logger.debug("Updating WmsReceiptOrderDetail object...")
        update_data = {'money': 38.0, 'remark': '密码希望出现有些组织北京朋友.'}

        # Modify the fields you want to update
        WmsReceiptOrderDetail.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsReceiptOrderDetail.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsReceiptOrderDetail(self):
        logger.debug("Deleting WmsReceiptOrderDetail object...")
        self.assertEqual(WmsReceiptOrderDetail.objects.count(), 1)
        # Delete the instance
        WmsReceiptOrderDetail.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsReceiptOrderDetail.objects.count(), 0)

    # Add more test methods as needed
