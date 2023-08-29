import logging
from django.test import TestCase
from WMS.models.receipt import WmsSupplier

logger = logging.getLogger(__name__)


class WmsSupplierTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsSupplier object...")
        obj = WmsSupplier.objects.create(is_show=False, create_time="1980-07-09 00:00:00",
                                         edit_time="1909-07-04 00:00:00", creator=None, editor=None,
                                         number="sVpIMI6piM", name="秦兰英", bank_name="自己中国应用.", bank_account="一下价格公司时间.",
                                         address="语言包括不要.", mobile_no="13524729192", tel_no="13460643941",
                                         contact="北京只有注意以上.", level="当然位置不过.", email="oshen@example.net",
                                         remark="音乐这个.")
        self.pk = obj.id
        self.assertEqual(WmsSupplier.objects.count(), 1)

    def test_update_WmsSupplier(self):
        logger.debug("Updating WmsSupplier object...")
        update_data = {'is_show': True, 'creator': None, 'editor': None, 'name': '王鹏', 'bank_account': '自己是一.',
                       'mobile_no': '15216966305', 'contact': '社会一次女人中文.', 'remark': '各种所有也是.'}

        # Modify the fields you want to update
        WmsSupplier.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsSupplier.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsSupplier(self):
        logger.debug("Deleting WmsSupplier object...")
        self.assertEqual(WmsSupplier.objects.count(), 1)
        # Delete the instance
        WmsSupplier.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsSupplier.objects.count(), 0)

    # Add more test methods as needed
