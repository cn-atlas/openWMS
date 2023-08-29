import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsItemViewSet
from api.filters.WMSFilter import WmsItemFilter
from api.tests.WMSTests import common
from WMS.models.item import WmsItem
import logging

logger = logging.getLogger(__name__)


class WmsItemTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        self.test_data = {'is_show': True, 'create_time': '1908-05-03 00:00:00', 'edit_time': '1921-07-20 00:00:00',
                          'creator': None, 'editor': None, 'abs_item': None, 'batch_number': 'xGlijmYGAI',
                          'produce_date': '1924-05-02 00:00:00', 'expiry_date': '1953-07-09 00:00:00',
                          'remark': '主要简介.'}
        self.update_data = {'batch_number': 'wFoqa9EL5k', 'remark': '记者时候以上评论.'}

        url = reverse('wmsitem-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsItem.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsItem.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = WmsItem.objects.get()

    def test_get_wmsitem_list(self):
        url = reverse('wmsitem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wmsitem(self):
        url = reverse('wmsitem-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = WmsItem.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsItem.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('wmsitem-list')
        search_key = random.choice(WmsItemViewSet.search_fields)
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
