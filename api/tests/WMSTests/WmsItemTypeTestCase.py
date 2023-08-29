import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsItemTypeViewSet
from api.filters.WMSFilter import WmsItemTypeFilter
from api.tests.WMSTests import common
from WMS.models.item import WmsItemType
import logging

logger = logging.getLogger(__name__)


class WmsItemTypeTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        self.test_data = {'is_show': True, 'create_time': '1949-08-05 00:00:00', 'edit_time': '2004-10-30 00:00:00',
                          'creator': None, 'editor': None, 'type_name': '音乐相关评论.', 'status': '4'}
        self.update_data = {'type_name': '如果计划新闻状态.', 'status': 'b'}

        url = reverse('wmsitemtype-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsItemType.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsItemType.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = WmsItemType.objects.get()

    def test_get_wmsitemtype_list(self):
        url = reverse('wmsitemtype-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wmsitemtype(self):
        url = reverse('wmsitemtype-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = WmsItemType.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsItemType.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('wmsitemtype-list')
        search_key = random.choice(WmsItemTypeViewSet.search_fields)
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
