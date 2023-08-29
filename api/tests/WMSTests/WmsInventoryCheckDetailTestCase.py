import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsInventoryCheckDetailViewSet
from api.filters.WMSFilter import WmsInventoryCheckDetailFilter
from api.tests.WMSTests import common
from WMS.models.check import WmsInventoryCheckDetail
import logging

logger = logging.getLogger(__name__)


class WmsInventoryCheckDetailTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        self.test_data = {'is_show': True, 'create_time': '1966-06-01 00:00:00', 'edit_time': '1995-04-21 00:00:00',
                          'creator': None, 'editor': None,
                          'inventory_check': common.get_link(common.create_inventory_check()),
                          'rack': common.get_link(common.create_rack()), 'item': common.get_link(common.create_item()),
                          'quantity': 74.0,
                          'check_quantity': 78.0, 'remark': '如此全部那么.'}
        self.update_data = {'quantity': 3.0, 'check_quantity': 25.0, 'remark': '人民工具程序.'}

        url = reverse('wmsinventorycheckdetail-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsInventoryCheckDetail.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsInventoryCheckDetail.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = WmsInventoryCheckDetail.objects.get()

    def test_bulk_create(self):
        bulk_data = [self.test_data]
        url = reverse('wmsinventorycheckdetail-list')
        response = self.client.post(url, bulk_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsInventoryCheckDetail.objects.count(), 2)

    def test_get_wmsinventorycheckdetail_list(self):
        url = reverse('wmsinventorycheckdetail-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wmsinventorycheckdetail(self):
        url = reverse('wmsinventorycheckdetail-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = WmsInventoryCheckDetail.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsInventoryCheckDetail.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('wmsinventorycheckdetail-list')
        search_key = random.choice(WmsInventoryCheckDetailViewSet.search_fields)
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
