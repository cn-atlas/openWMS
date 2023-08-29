import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsShipmentOrderDetailViewSet
from api.filters.WMSFilter import WmsShipmentOrderDetailFilter
from api.tests.WMSTests import common
from WMS.models.shipment import WmsShipmentOrderDetail
import logging

logger = logging.getLogger(__name__)


class WmsShipmentOrderDetailTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        self.test_data = {'is_show': True, 'create_time': '1951-02-13 00:00:00', 'edit_time': '1944-10-02 00:00:00',
                          'creator': None, 'editor': None, 'shipment_order': common.get_link(common.create_shipment()),
                          'inventory': None, 'plan_quantity': 39.0, 'real_quantity': 3.0,
                          'rack': common.get_link(common.create_rack()),
                          'money': 41.0, 'status': 95, 'remark': '业务本站一般.'}
        self.update_data = {'plan_quantity': 42.0, 'real_quantity': 43.0, 'money': 23.0, 'status': 29,
                            'remark': '的人可能是否.'}

        url = reverse('wmsshipmentorderdetail-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsShipmentOrderDetail.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsShipmentOrderDetail.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = WmsShipmentOrderDetail.objects.get()

    def test_bulk_create(self):
        bulk_data = [self.test_data]
        url = reverse('wmsshipmentorderdetail-list')
        response = self.client.post(url, bulk_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsShipmentOrderDetail.objects.count(), 2)

    def test_get_wmsshipmentorderdetail_list(self):
        url = reverse('wmsshipmentorderdetail-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wmsshipmentorderdetail(self):
        url = reverse('wmsshipmentorderdetail-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = WmsShipmentOrderDetail.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsShipmentOrderDetail.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('wmsshipmentorderdetail-list')
        search_key = random.choice(WmsShipmentOrderDetailViewSet.search_fields)
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
