import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsRackViewSet
from api.filters.WMSFilter import WmsRackFilter
from api.tests.WMSTests import common
from WMS.models.warehouse import WmsRack
import logging

logger = logging.getLogger(__name__)


class WmsRackTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        self.test_data = {'is_show': True, 'create_time': '1949-07-26 00:00:00', 'edit_time': '2009-09-05 00:00:00',
                          'creator': None, 'editor': None, 'warehouse': None,
                          'area': common.get_link(common.create_area()),
                          'number': 'ULMURonnNx', 'name': '史玉珍', 'remark': '学习所以市场.'}
        self.update_data = {'number': 'CU2DEBSB7p', 'name': '段秀芳', 'remark': '的是起来作者.'}

        url = reverse('wmsrack-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsRack.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsRack.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = WmsRack.objects.get()

    def test_get_wmsrack_list(self):
        url = reverse('wmsrack-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wmsrack(self):
        url = reverse('wmsrack-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = WmsRack.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsRack.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('wmsrack-list')
        search_key = random.choice(WmsRackViewSet.search_fields)
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
