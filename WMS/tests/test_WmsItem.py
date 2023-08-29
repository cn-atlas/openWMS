import logging
from django.test import TestCase
from WMS.models.item import WmsItem

logger = logging.getLogger(__name__)


class WmsItemTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsItem object...")
        obj = WmsItem.objects.create(is_show=True, create_time="2021-08-23 00:00:00", edit_time="1963-10-11 00:00:00",
                                     creator=None, editor=None, abs_item=None, batch_number="SEcRgs8wXb",
                                     produce_date="1943-07-20 00:00:00", expiry_date="1987-07-23 00:00:00",
                                     remark="数据表示安全文化地区北京市场.")
        self.pk = obj.id
        self.assertEqual(WmsItem.objects.count(), 1)

    def test_update_WmsItem(self):
        logger.debug("Updating WmsItem object...")
        update_data = {'editor': None}

        # Modify the fields you want to update
        WmsItem.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsItem.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsItem(self):
        logger.debug("Deleting WmsItem object...")
        self.assertEqual(WmsItem.objects.count(), 1)
        # Delete the instance
        WmsItem.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsItem.objects.count(), 0)

    # Add more test methods as needed
