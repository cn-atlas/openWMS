import logging
from django.test import TestCase
from WMS.models.item import WmsItemType

logger = logging.getLogger(__name__)


class WmsItemTypeTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsItemType object...")
        obj = WmsItemType.objects.create(is_show=True, create_time="1957-08-02 00:00:00",
                                         edit_time="1925-11-16 00:00:00", creator=None, editor=None,
                                         type_name="方面由于那些记者标准你的.", status="0")
        self.pk = obj.id
        self.assertEqual(WmsItemType.objects.count(), 1)

    def test_update_WmsItemType(self):
        logger.debug("Updating WmsItemType object...")
        update_data = {"type_name": "xxxxx."}

        # Modify the fields you want to update
        WmsItemType.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsItemType.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsItemType(self):
        logger.debug("Deleting WmsItemType object...")
        self.assertEqual(WmsItemType.objects.count(), 1)
        # Delete the instance
        WmsItemType.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsItemType.objects.count(), 0)

    # Add more test methods as needed
