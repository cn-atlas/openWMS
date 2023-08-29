import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsInventoryViewSet
from api.filters.WMSFilter import WmsInventoryFilter
from api.tests.WMSTests import common
from WMS.models.inventory import WmsInventory
import logging

logger = logging.getLogger(__name__)


class WmsInventoryTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)

    #     self.test_data = {'is_show': True, 'create_time': '2012-11-19 00:00:00', 'edit_time': '1908-02-12 00:00:00', 'creator': None, 'editor': None, 'rack': None, 'item': None, 'quantity': 84.0, 'remark': '这里由于什么.'}
    #     self.update_data = {'quantity': 41.0, 'remark': '世界帮助关于设备.'}
    #
    #     url = reverse('wmsinventory-list')
    #     # logger.debug(self.client)
    #     response = self.client.post(url, self.test_data, format='json')
    #     # logger.debug(url, response.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(WmsInventory.objects.count(), 1)
    #     # update_data 可以避开 datetime field
    #     key = random.choice(list(self.update_data.keys()))
    #     value = getattr(WmsInventory.objects.get(), key)
    #     self.assertEqual(value, self.test_data.get(key))
    #     self.obj = WmsInventory.objects.get()
    #
    # def test_get_wmsinventory_list(self):
    #     url = reverse('wmsinventory-list')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_update_wmsinventory(self):
    #     url = reverse('wmsinventory-detail', args=[self.obj.id])
    #     response = self.client.patch(url, self.update_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.obj = WmsInventory.objects.get()
    #     key = random.choice(list(self.update_data.keys()))
    #     value = getattr(WmsInventory.objects.get(), key)
    #     self.assertEqual(value, self.update_data.get(key))
    #
    # def test_search(self):
    #     url = reverse('wmsinventory-list')
    #     search_key = random.choice(WmsInventoryViewSet.search_fields)
    #     k = self.update_data.get(search_key, None) if not self.update_data.get(search_key, None) else         self.test_data.get(search_key, "")
    #     full_url = url + "?search=" + k
    #     response = self.client.get(full_url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter(self):
        pass

    def tearDown(self) -> None:
        pass
