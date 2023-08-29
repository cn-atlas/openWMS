import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsReceiptOrderViewSet
from api.filters.WMSFilter import WmsReceiptOrderFilter
from api.tests.WMSTests import common
from WMS.models.receipt import WmsReceiptOrder
import logging

logger = logging.getLogger(__name__)


class WmsReceiptOrderTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        self.test_data = {'is_show': True, 'create_time': '1964-01-05 00:00:00', 'edit_time': '1933-08-15 00:00:00',
                          'creator': None, 'editor': None, 'number': 'dHsLpAEl0h', 'receipt_type': 83, 'supplier': None,
                          'order_no': '的人准备.', 'payable_amount': 67.0, 'status': 0, 'remark': '社区孩子.'}
        self.update_data = {'number': 'vHMM3B4zOK', 'receipt_type': 67, 'order_no': '现在出来一种.', 'payable_amount': 83.0,
                            'remark': '活动更新.'}

        url = reverse('wmsreceiptorder-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsReceiptOrder.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsReceiptOrder.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = WmsReceiptOrder.objects.get()

    def test_get_wmsreceiptorder_list(self):
        url = reverse('wmsreceiptorder-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wmsreceiptorder(self):
        url = reverse('wmsreceiptorder-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = WmsReceiptOrder.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsReceiptOrder.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('wmsreceiptorder-list')
        search_key = random.choice(WmsReceiptOrderViewSet.search_fields)
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
