import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsInventoryHistoryViewSet
from api.filters.WMSFilter import WmsInventoryHistoryFilter
from api.tests.WMSTests import common
from WMS.models.inventory import WmsInventoryHistory
import logging

logger = logging.getLogger(__name__)


class WmsInventoryHistoryTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)

    #     self.test_data = {'is_show': True, 'create_time': '1942-01-02 00:00:00', 'edit_time': '1940-01-18 00:00:00', 'creator': None, 'editor': None, 'inventory_movement': None, 'inventory_receipt_order': None, 'inventory_shipment_order': None, 'form_type': 39, 'number_type': '6HOsFv2bLT', 'item': None, 'rack': None, 'quantity': 73.0, 'balance': 13.0, 'remark': '发生主要影响.'}
    #     self.update_data = {'form_type': 86, 'number_type': 'A6ndOMQONC', 'quantity': 91.0, 'balance': 1.0, 'remark': '一种有限工作.'}
    #
    #     url = reverse('wmsinventoryhistory-list')
    #     # logger.debug(self.client)
    #     response = self.client.post(url, self.test_data, format='json')
    #     # logger.debug(url, response.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(WmsInventoryHistory.objects.count(), 1)
    #     # update_data 可以避开 datetime field
    #     key = random.choice(list(self.update_data.keys()))
    #     value = getattr(WmsInventoryHistory.objects.get(), key)
    #     self.assertEqual(value, self.test_data.get(key))
    #     self.obj = WmsInventoryHistory.objects.get()
    #
    # def test_get_wmsinventoryhistory_list(self):
    #     url = reverse('wmsinventoryhistory-list')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_update_wmsinventoryhistory(self):
    #     url = reverse('wmsinventoryhistory-detail', args=[self.obj.id])
    #     response = self.client.patch(url, self.update_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.obj = WmsInventoryHistory.objects.get()
    #     key = random.choice(list(self.update_data.keys()))
    #     value = getattr(WmsInventoryHistory.objects.get(), key)
    #     self.assertEqual(value, self.update_data.get(key))
    #
    # def test_search(self):
    #     url = reverse('wmsinventoryhistory-list')
    #     search_key = random.choice(WmsInventoryHistoryViewSet.search_fields)
    #     k = self.update_data.get(search_key, None) if not self.update_data.get(search_key, None) else         self.test_data.get(search_key, "")
    #     full_url = url + "?search=" + k
    #     response = self.client.get(full_url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #
    # def test_filter(self):
    #     pass
    #
    def tearDown(self) -> None:
        pass
