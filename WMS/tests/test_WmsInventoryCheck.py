import logging
from django.test import TestCase
from WMS.models.check import WmsInventoryCheck

logger = logging.getLogger(__name__)


class WmsInventoryCheckTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsInventoryCheck object...")
        obj = WmsInventoryCheck.objects.create(is_show=True, create_time="1997-12-06 00:00:00",
                                               edit_time="1956-12-15 00:00:00", creator=None, editor=None,
                                               is_checked=False, check_time="1941-04-06 00:00:00", check_user=None,
                                               check_note="以下提供电脑特别包括技术状态.", number="cnKD7OKM7M",
                                               inventory_check_type=86, inventory_check_status=99,
                                               inventory_check_total=71.0, warehouse=None, area=None, rack=None,
                                               attachment=None, remark="必须安全直接作为更多重要.")
        self.pk = obj.id
        self.assertEqual(WmsInventoryCheck.objects.count(), 1)

    def test_update_WmsInventoryCheck(self):
        logger.debug("Updating WmsInventoryCheck object...")
        update_data = {'is_show': True, 'is_checked': True, 'check_user': None, 'check_note': '喜欢游戏地址网站也是能够.',
                       'number': 'U0oUk2afNt', 'inventory_check_type': 6, 'inventory_check_status': 76,
                       'inventory_check_total': 32.0, 'warehouse': None, 'area': None}

        # Modify the fields you want to update
        WmsInventoryCheck.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsInventoryCheck.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsInventoryCheck(self):
        logger.debug("Deleting WmsInventoryCheck object...")
        self.assertEqual(WmsInventoryCheck.objects.count(), 1)
        # Delete the instance
        WmsInventoryCheck.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsInventoryCheck.objects.count(), 0)

    # Add more test methods as needed
