import logging
from django.test import TestCase
from WMS.models.warehouse import WmsRack, WmsArea, WmsWarehouse
from WMS.models.warehouse import WmsRack

logger = logging.getLogger(__name__)


class WmsRackTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsRack object...")
        warehouse_obj = WmsWarehouse.objects.create(number="warehouse1", name="sdkfh")
        area_obj = WmsArea.objects.create(number="area12", name="area12", warehouse=warehouse_obj)
        obj = WmsRack.objects.create(is_show=False, create_time="1996-09-05 00:00:00", edit_time="1932-06-28 00:00:00",
                                     creator=None, editor=None, area=area_obj, number="BcXaItd6jX",
                                     name="刘玉兰", remark="比较他的结果项目类别能力已经.")
        self.pk = obj.id
        self.assertEqual(WmsRack.objects.count(), 1)

    def test_update_WmsRack(self):
        logger.debug("Updating WmsRack object...")
        update_data = {'creator': None, 'number': 'eIR9wYA0OK', 'name': '许强'}

        # Modify the fields you want to update
        WmsRack.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsRack.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsRack(self):
        logger.debug("Deleting WmsRack object...")
        self.assertEqual(WmsRack.objects.count(), 1)
        # Delete the instance
        WmsRack.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsRack.objects.count(), 0)

    # Add more test methods as needed
