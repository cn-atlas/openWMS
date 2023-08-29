import logging
from django.test import TestCase
from WMS.models.item import WmsAbsItem

logger = logging.getLogger(__name__)


class WmsAbsItemTestCase(TestCase):
    def setUp(self):
        logger.debug("Creating WmsAbsItem object...")
        obj = WmsAbsItem.objects.create(is_show=False, create_time="1950-08-09 00:00:00",
                                        edit_time="1988-10-09 00:00:00", creator=None, editor=None, number="wbKmEbgXvF",
                                        name="王淑华", specs="继续威望来自查看选择建设已经.", model="来源名称开始目前决定名称.",
                                        manufacturer="论坛女人空间看到主题对于.", item_type=None, unit="只是回复可能学习文件有关提高.",
                                        quantity=9.0, total_number=52.0, remark="销售经验首页学校.")
        self.pk = obj.id
        self.assertEqual(WmsAbsItem.objects.count(), 1)

    def test_update_WmsAbsItem(self):
        logger.debug("Updating WmsAbsItem object...")
        update_data = {'creator': None, 'name': '佘健', 'manufacturer': '汽车上海名称现在要求.', 'unit': '方式密码喜欢直接还是图片.',
                       'quantity': 10.0, 'total_number': 52.0}

        # Modify the fields you want to update
        WmsAbsItem.objects.filter(pk=self.pk).update(**update_data)

        instance = WmsAbsItem.objects.get(pk=self.pk)
        for k, v in update_data.items():
            self.assertEqual(getattr(instance, k), update_data[k])

    def test_delete_WmsAbsItem(self):
        logger.debug("Deleting WmsAbsItem object...")
        self.assertEqual(WmsAbsItem.objects.count(), 1)
        # Delete the instance
        WmsAbsItem.objects.filter(pk=self.pk).delete()
        self.assertEqual(WmsAbsItem.objects.count(), 0)

    # Add more test methods as needed
