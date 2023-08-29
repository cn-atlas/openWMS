import logging
from django.test import TestCase
from WMS.models.warehouse import WmsWarehouse

logger = logging.getLogger(__name__)


class WmsWarehouseTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsWarehouse object...")
        obj = WmsWarehouse.objects.create(is_show=True, create_time="1975-08-29 00:00:00",
                                          edit_time="2021-01-19 00:00:00", creator=None, editor=None,
                                          number="FhBno8qgyJ", name="林玉珍", remark="不是免费觉得信息个人的话应该部分.")
        self.pk = obj.id
        self.assertEqual(WmsWarehouse.objects.count(), 1)

    def test_update_WmsWarehouse(self):
        logger.debug("Updating WmsWarehouse object...")
        update_data = {'name': '朱健'}

        # Modify the fields you want to update
        WmsWarehouse.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsWarehouse.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsWarehouse(self):
        logger.debug("Deleting WmsWarehouse object...")
        self.assertEqual(WmsWarehouse.objects.count(), 1)
        # Delete the instance
        WmsWarehouse.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsWarehouse.objects.count(), 0)

    # Add more test methods as needed
