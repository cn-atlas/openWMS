import logging
from django.test import TestCase
from WMS.models.shipment import WmsShipmentOrder

logger = logging.getLogger(__name__)


class WmsShipmentOrderTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsShipmentOrder object...")
        obj = WmsShipmentOrder.objects.create(is_show=True, create_time="1993-09-19 00:00:00",
                                              edit_time="2008-07-03 00:00:00", creator=None, editor=None,
                                              is_checked=True, check_time="1930-10-29 00:00:00", check_user=None,
                                              check_note="到了感觉功能次数.", number="7E2vNyfslj", shipment_order_type=70,
                                              order_no="有些次数主题应用对于这个国家.", to_customer="发生知道是一注册.", to_user=None,
                                              receivable_amount=46.0, status=85, remark="继续出来决定目前.")
        self.pk = obj.id
        self.assertEqual(WmsShipmentOrder.objects.count(), 1)

    def test_update_WmsShipmentOrder(self):
        logger.debug("Updating WmsShipmentOrder object...")
        update_data = {'is_show': True, 'number': 'JuMuEXzt7D', 'shipment_order_type': 14}

        # Modify the fields you want to update
        WmsShipmentOrder.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsShipmentOrder.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsShipmentOrder(self):
        logger.debug("Deleting WmsShipmentOrder object...")
        self.assertEqual(WmsShipmentOrder.objects.count(), 1)
        # Delete the instance
        WmsShipmentOrder.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsShipmentOrder.objects.count(), 0)

    # Add more test methods as needed
