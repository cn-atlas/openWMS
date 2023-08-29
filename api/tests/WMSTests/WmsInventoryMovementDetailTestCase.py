import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsInventoryMovementDetailViewSet
from api.filters.WMSFilter import WmsInventoryMovementDetailFilter
from api.tests.WMSTests import common
from WMS.models.movement import WmsInventoryMovementDetail
import logging

logger = logging.getLogger(__name__)


class WmsInventoryMovementDetailTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        self.test_data = {'is_show': True, 'create_time': '2011-05-17 00:00:00', 'edit_time': '1982-03-01 00:00:00',
                          'creator': None, 'editor': None,
                          'inventory_movement': common.get_link(common.create_inventory_movement()),
                          'inventory': None, 'plan_quantity': 24.0, 'real_quantity': 88.0,
                          'source_rack': common.get_link(common.create_rack()),
                          'target_rack': common.get_link(common.create_rack()),
                          'remark': '位置我们日本为什.'}
        self.update_data = {'plan_quantity': 77.0, 'real_quantity': 82.0, 'remark': '正在网络这里.'}

        url = reverse('wmsinventorymovementdetail-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsInventoryMovementDetail.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsInventoryMovementDetail.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = WmsInventoryMovementDetail.objects.get()

    def test_bulk_create(self):
        bulk_data = [self.test_data]
        url = reverse('wmsinventorymovementdetail-list')
        response = self.client.post(url, bulk_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsInventoryMovementDetail.objects.count(), 2)

    def test_get_wmsinventorymovementdetail_list(self):
        url = reverse('wmsinventorymovementdetail-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wmsinventorymovementdetail(self):
        url = reverse('wmsinventorymovementdetail-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = WmsInventoryMovementDetail.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsInventoryMovementDetail.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('wmsinventorymovementdetail-list')
        search_key = random.choice(WmsInventoryMovementDetailViewSet.search_fields)
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
