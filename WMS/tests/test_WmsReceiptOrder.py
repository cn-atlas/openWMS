import logging
from django.test import TestCase
from WMS.models.receipt import WmsReceiptOrder

logger = logging.getLogger(__name__)


class WmsReceiptOrderTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsReceiptOrder object...")
        obj = WmsReceiptOrder.objects.create(is_show=True, create_time="2012-07-24 00:00:00",
                                             edit_time="1961-10-28 00:00:00", creator=None, editor=None,
                                             number="1gG6ApUfbw", receipt_type=45, supplier=None,
                                             order_no="主题发现一样应该今天生活.", payable_amount=39.0, status=94,
                                             remark="经验特别一样阅读拥有内容其他.")
        self.pk = obj.id
        self.assertEqual(WmsReceiptOrder.objects.count(), 1)

    def test_update_WmsReceiptOrder(self):
        logger.debug("Updating WmsReceiptOrder object...")
        update_data = {'supplier': None}

        # Modify the fields you want to update
        WmsReceiptOrder.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsReceiptOrder.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsReceiptOrder(self):
        logger.debug("Deleting WmsReceiptOrder object...")
        self.assertEqual(WmsReceiptOrder.objects.count(), 1)
        # Delete the instance
        WmsReceiptOrder.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsReceiptOrder.objects.count(), 0)

    # Add more test methods as needed
