import logging
from django.test import TestCase
from WMS.models.warehouse import WmsRack, WmsArea, WmsWarehouse
from WMS.models.movement import WmsInventoryMovement, WmsInventoryMovementDetail

logger = logging.getLogger(__name__)


class WmsInventoryMovementDetailTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsInventoryMovementDetail object...")
        movement_obj = WmsInventoryMovement.objects.create(number="sdflnkdsn")
        warehouse_obj = WmsWarehouse.objects.create(number="warehouse1", name="sdkfh")
        area_obj = WmsArea.objects.create(number="area12", name="area12", warehouse=warehouse_obj)
        rack_obj1 = WmsRack.objects.create(number="rack1", name="rack1", area=area_obj)
        rack_obj2 = WmsRack.objects.create(number="rack2", name="rack2", area=area_obj)
        obj = WmsInventoryMovementDetail.objects.create(is_show=True, create_time="1915-04-06 00:00:00",
                                                        edit_time="1966-12-12 00:00:00", creator=None, editor=None,
                                                        inventory_movement=movement_obj, inventory=None,
                                                        plan_quantity=30.0,
                                                        real_quantity=69.0, source_rack=rack_obj1,
                                                        target_rack=rack_obj2,
                                                        status=45, remark="开始孩子空间方式如果重要谢谢.")
        self.pk = obj.id
        self.assertEqual(WmsInventoryMovementDetail.objects.count(), 1)

    def test_update_WmsInventoryMovementDetail(self):
        logger.debug("Updating WmsInventoryMovementDetail object...")
        update_data = {'editor': None, 'plan_quantity': 22.0, 'status': 87,
                       'remark': '就是自己文件准备企业不断.'}

        # Modify the fields you want to update
        WmsInventoryMovementDetail.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsInventoryMovementDetail.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsInventoryMovementDetail(self):
        logger.debug("Deleting WmsInventoryMovementDetail object...")
        self.assertEqual(WmsInventoryMovementDetail.objects.count(), 1)
        # Delete the instance
        WmsInventoryMovementDetail.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsInventoryMovementDetail.objects.count(), 0)

    # Add more test methods as needed
