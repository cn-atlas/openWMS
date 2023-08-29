import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsShipmentOrderViewSet
from api.filters.WMSFilter import WmsShipmentOrderFilter
from api.tests.WMSTests import common
from WMS.models.shipment import WmsShipmentOrder
import logging

logger = logging.getLogger(__name__)


class WmsShipmentOrderTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        # is_checked 为 False 的时候 status 必须是 3， 否则不测试
        self.test_data = {'is_show': True, 'create_time': '1924-10-16 00:00:00', 'edit_time': '1930-12-03 00:00:00',
                          'creator': None, 'editor': None, 'is_checked': False, 'check_time': '1957-11-20 00:00:00',
                          'check_user': None, 'check_note': '主题感觉比较这里.', 'number': 'XRlw903fIl',
                          'shipment_order_type': 49, 'order_no': '有关注意.', 'to_customer': '注册详细.', 'to_user': None,
                          'receivable_amount': 31.0, 'remark': '电话登录.'}
        self.update_data = {'check_note': '她的管理广告位置.', 'number': '6FaHK1SMv0',
                            'shipment_order_type': 24, 'order_no': '中文一下历史.', 'to_customer': '大家正在.',
                            'receivable_amount': 67.0, 'remark': '合作地方日本女人.'}

        url = reverse('wmsshipmentorder-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsShipmentOrder.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsShipmentOrder.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = WmsShipmentOrder.objects.get()

    def test_get_wmsshipmentorder_list(self):
        url = reverse('wmsshipmentorder-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wmsshipmentorder(self):
        url = reverse('wmsshipmentorder-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = WmsShipmentOrder.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsShipmentOrder.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('wmsshipmentorder-list')
        search_key = random.choice(WmsShipmentOrderViewSet.search_fields)
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
