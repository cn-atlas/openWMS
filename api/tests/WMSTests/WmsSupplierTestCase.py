import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsSupplierViewSet
from api.filters.WMSFilter import WmsSupplierFilter
from api.tests.WMSTests import common
from WMS.models.receipt import WmsSupplier
import logging

logger = logging.getLogger(__name__)


class WmsSupplierTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        self.test_data = {'is_show': True, 'create_time': '1984-11-13 00:00:00', 'edit_time': '1910-10-14 00:00:00',
                          'creator': None, 'editor': None, 'number': 'IhFdxws43x', 'name': '李玉', 'bank_name': '发现这里到了.',
                          'bank_account': '业务积分.', 'address': '女人主要今天因此.', 'mobile_no': '13293062894',
                          'tel_no': '18541809188', 'contact': '以上回复.', 'level': '看到地址位置人民.',
                          'email': 'weimo@example.com', 'remark': '更新联系显示自己.'}
        self.update_data = {'number': 'GHeunTH1Xw', 'name': '李金凤', 'bank_name': '一样完成.', 'bank_account': '新闻同时完成资源.',
                            'address': '有些登录方面.', 'mobile_no': '18604158600', 'tel_no': '14755723246',
                            'contact': '一切如果.', 'level': '有限资料教育安全.', 'email': 'hyuan@example.org',
                            'remark': '注册会员作为最新.'}

        url = reverse('wmssupplier-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsSupplier.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsSupplier.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = WmsSupplier.objects.get()

    def test_get_wmssupplier_list(self):
        url = reverse('wmssupplier-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wmssupplier(self):
        url = reverse('wmssupplier-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = WmsSupplier.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsSupplier.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('wmssupplier-list')
        search_key = random.choice(WmsSupplierViewSet.search_fields)
        k = self.update_data.get(search_key, None) if not self.update_data.get(search_key,
                                                                               None) else self.test_data.get(search_key,
                                                                                                             "")
        full_url = url + "?search=" + k
        response = self.client.get(full_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter(self):
        pass

    def tearDown(self) -> None:
        pass
