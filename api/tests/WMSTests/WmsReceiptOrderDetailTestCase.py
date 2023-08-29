import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsReceiptOrderDetailViewSet
from api.filters.WMSFilter import WmsReceiptOrderDetailFilter
from api.tests.WMSTests import common
from WMS.models.receipt import WmsReceiptOrderDetail
import logging

logger = logging.getLogger(__name__)


class WmsReceiptOrderDetailTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        self.test_data = {'is_show': True, 'create_time': '1975-04-07 00:00:00', 'edit_time': '1919-08-13 00:00:00',
                          'creator': None, 'editor': None, 'receipt_order': common.get_link(common.create_receipt()),
                          'item': common.get_link(common.create_item()), 'plan_quantity': 24.0, 'real_quantity': 6.0,
                          'rack': common.get_link(common.create_rack()), 'money': 65.0,
                          'status': 24, 'remark': '开始朋友.'}
        self.update_data = {'plan_quantity': 94.0, 'real_quantity': 27.0, 'money': 31.0, 'status': 99,
                            'remark': '的是公司全部重要.'}

        url = reverse('wmsreceiptorderdetail-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsReceiptOrderDetail.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsReceiptOrderDetail.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = WmsReceiptOrderDetail.objects.get()

    def test_bulk_create(self):
        bulk_data = [self.test_data]
        url = reverse('wmsreceiptorderdetail-list')
        response = self.client.post(url, bulk_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsReceiptOrderDetail.objects.count(), 2)

    def test_get_wmsreceiptorderdetail_list(self):
        url = reverse('wmsreceiptorderdetail-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wmsreceiptorderdetail(self):
        url = reverse('wmsreceiptorderdetail-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = WmsReceiptOrderDetail.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsReceiptOrderDetail.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('wmsreceiptorderdetail-list')
        search_key = random.choice(WmsReceiptOrderDetailViewSet.search_fields)
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
