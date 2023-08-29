import random, copy
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsInventoryCheckViewSet
from api.filters.WMSFilter import WmsInventoryCheckFilter
from api.tests.WMSTests import common
from WMS.models.check import WmsInventoryCheck
import logging

logger = logging.getLogger(__name__)


class WmsInventoryCheckTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        self.test_data = {'is_show': True, 'create_time': '1974-10-16 00:00:00', 'edit_time': '1987-03-09 00:00:00',
                          'creator': None, 'editor': None, 'is_checked': True, 'check_time': '1949-02-15 00:00:00',
                          'check_user': None, 'check_note': '其他主要一样希望.', 'number': 'uxWbOSdz9c',
                          'inventory_check_type': 3, 'inventory_check_status': 11, 'inventory_check_total': 77.0,
                          'warehouse': common.get_link(common.create_warehouse()),
                          'area': common.get_link(common.create_area()), 'rack': common.get_link(common.create_rack()),
                          'item': [common.get_link(common.create_item())], 'attachment': None, 'remark': '这里标准的话而且.'}
        # is_checked 为 False 的时候 status 必须是 3
        self.update_data = {'is_checked': False, 'check_note': '国际广告业务业务.', 'number': 'wNojFKIx9N',
                            'inventory_check_status': 11, 'inventory_check_total': 21.0, 'remark': '积分说明没有.'}
        self.test_data_401 = copy.deepcopy(self.test_data)
        self.test_data_401["item"] = []
        url = reverse('wmsinventorycheck-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsInventoryCheck.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsInventoryCheck.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = WmsInventoryCheck.objects.get()

    def test_type_not_cp_option(self):
        url = reverse('wmsinventorycheck-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data_401, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(WmsInventoryCheck.objects.count(), 1)

    def test_get_wmsinventorycheck_list(self):
        url = reverse('wmsinventorycheck-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wmsinventorycheck(self):
        url = reverse('wmsinventorycheck-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = WmsInventoryCheck.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsInventoryCheck.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('wmsinventorycheck-list')
        search_key = random.choice(WmsInventoryCheckViewSet.search_fields)
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
