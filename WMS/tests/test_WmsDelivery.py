import logging
from django.test import TestCase
from WMS.models.shipment import WmsDelivery

logger = logging.getLogger(__name__)


class WmsDeliveryTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsDelivery object...")
        obj = WmsDelivery.objects.create(is_show=True, create_time="2006-09-22 00:00:00",
                                         edit_time="1966-05-11 00:00:00", creator=None, editor=None,
                                         shipment_order=None, carrier="北京软件进入单位大小点击.",
                                         delivery_date="1988-08-11 00:00:00", tracking_no="作品各种还是可能电脑.",
                                         remark="看到当然特别方式介绍.")
        self.pk = obj.id
        self.assertEqual(WmsDelivery.objects.count(), 1)

    def test_update_WmsDelivery(self):
        logger.debug("Updating WmsDelivery object...")
        update_data = {'creator': None, 'tracking_no': '产品行业类型原因市场网上.', 'remark': '详细名称位置社区政府.'}

        # Modify the fields you want to update
        WmsDelivery.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsDelivery.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsDelivery(self):
        logger.debug("Deleting WmsDelivery object...")
        self.assertEqual(WmsDelivery.objects.count(), 1)
        # Delete the instance
        WmsDelivery.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsDelivery.objects.count(), 0)

    # Add more test methods as needed
