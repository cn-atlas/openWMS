import logging
from django.test import TestCase
from WMS.models.movement import WmsInventoryMovement

logger = logging.getLogger(__name__)


class WmsInventoryMovementTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsInventoryMovement object...")
        obj = WmsInventoryMovement.objects.create(is_show=False, create_time="1943-10-02 00:00:00",
                                                  edit_time="1964-06-03 00:00:00", creator=None, editor=None,
                                                  is_checked=True, check_time="1983-11-21 00:00:00", check_user=None,
                                                  check_note="通过专业行业推荐必须非常程序.", number="XJPVFhdhv3", source_rack=None,
                                                  target_rack=None, status=18, remark="运行已经网上方式记者.")
        self.pk = obj.id
        self.assertEqual(WmsInventoryMovement.objects.count(), 1)

    def test_update_WmsInventoryMovement(self):
        logger.debug("Updating WmsInventoryMovement object...")
        update_data = {'creator': None, 'check_user': None, 'check_note': '所有实现在线或者过程需要类别.', 'number': 'la5ihkWWIb',
                       'status': 66, 'remark': '发布不是威望.'}

        # Modify the fields you want to update
        WmsInventoryMovement.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsInventoryMovement.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsInventoryMovement(self):
        logger.debug("Deleting WmsInventoryMovement object...")
        self.assertEqual(WmsInventoryMovement.objects.count(), 1)
        # Delete the instance
        WmsInventoryMovement.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsInventoryMovement.objects.count(), 0)

    # Add more test methods as needed
