import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsWarehouseViewSet
from api.filters.WMSFilter import WmsWarehouseFilter
from api.tests.WMSTests import common
from WMS.models.warehouse import WmsWarehouse
import logging

logger = logging.getLogger(__name__)


class WmsWarehouseTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        self.test_data = {'is_show': True, 'create_time': '2021-08-30 00:00:00', 'edit_time': '1992-09-09 00:00:00',
                          'creator': None, 'editor': None, 'number': 'TJ3HXjZlG1', 'name': '王坤', 'remark': '北京发展那个拥有.'}
        self.update_data = {'number': 'yRoFKKVnU2', 'name': '唐旭', 'remark': '学生工具.'}

        url = reverse('wmswarehouse-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsWarehouse.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsWarehouse.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = WmsWarehouse.objects.get()

    def test_get_wmswarehouse_list(self):
        url = reverse('wmswarehouse-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wmswarehouse(self):
        url = reverse('wmswarehouse-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = WmsWarehouse.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsWarehouse.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('wmswarehouse-list')
        search_key = random.choice(WmsWarehouseViewSet.search_fields)
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
