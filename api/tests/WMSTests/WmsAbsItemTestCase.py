import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsAbsItemViewSet
from api.filters.WMSFilter import WmsAbsItemFilter
from api.tests.WMSTests import common
from WMS.models.item import WmsAbsItem
import logging

logger = logging.getLogger(__name__)


class WmsAbsItemTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        self.test_data = {'is_show': True, 'create_time': '2002-01-04 00:00:00', 'edit_time': '1975-11-04 00:00:00',
                          'creator': None, 'editor': None, 'number': '0D7e6tSk0x', 'name': '潘梅', 'specs': '影响进行是一类别.',
                          'model': '应该登录.', 'manufacturer': '当前发布运行很多.', 'item_type': None, 'unit': '问题责任能够.',
                          'quantity': 17.0, 'total_number': 31.0, 'remark': '需要原因全国.'}
        self.update_data = {'number': '8Mor3tYTdE', 'name': '蔡雪梅', 'specs': '他的还有查看.', 'model': '其他分析如此.',
                            'manufacturer': '增加中心.', 'unit': '本站在线.', 'quantity': 4.0, 'total_number': 57.0,
                            'remark': '结果一些.'}

        url = reverse('wmsabsitem-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsAbsItem.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsAbsItem.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = WmsAbsItem.objects.get()

    def test_get_wmsabsitem_list(self):
        url = reverse('wmsabsitem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wmsabsitem(self):
        url = reverse('wmsabsitem-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = WmsAbsItem.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsAbsItem.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('wmsabsitem-list')
        search_key = random.choice(WmsAbsItemViewSet.search_fields)
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
