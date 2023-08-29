import logging
from django.test import TestCase
from WMS.models.warehouse import WmsWarehouse, WmsArea

logger = logging.getLogger(__name__)


class WmsAreaTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsArea object...")
        warehouse_obj = WmsWarehouse.objects.create(number="warehouse1", name="sdkfh")
        obj = WmsArea.objects.create(is_show=False, create_time="1943-07-22 00:00:00", edit_time="1993-03-05 00:00:00",
                                     creator=None, editor=None, number="AGm0pS1e1U", name="李玉梅",
                                     warehouse=warehouse_obj,
                                     remark="部门威望不能的人以后公司项目.")
        self.pk = obj.id
        self.assertEqual(WmsArea.objects.count(), 1)

    def test_update_WmsArea(self):
        logger.debug("Updating WmsArea object...")
        update_data = {'creator': None, 'remark': '汽车以下设计技术.'}

        # Modify the fields you want to update
        WmsArea.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsArea.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsArea(self):
        logger.debug("Deleting WmsArea object...")
        self.assertEqual(WmsArea.objects.count(), 1)
        # Delete the instance
        WmsArea.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsArea.objects.count(), 0)

    # Add more test methods as needed
