import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsDeliveryViewSet
from api.filters.WMSFilter import WmsDeliveryFilter
from api.tests.WMSTests import common
from WMS.models.shipment import WmsDelivery
import logging

logger = logging.getLogger(__name__)


class WmsDeliveryTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        self.test_data = {'is_show': True, 'create_time': '1938-12-24 00:00:00', 'edit_time': '2005-09-28 00:00:00',
                          'creator': None, 'editor': None, 'shipment_order': None, 'carrier': '是否文化.',
                          'delivery_date': '1968-07-30 00:00:00', 'tracking_no': '可能就是作为开发.', 'remark': '他们朋友.'}
        self.update_data = {'carrier': '最后欢迎生活单位.', 'tracking_no': '生产如此你的大家.', 'remark': '生产国内那些.'}

        url = reverse('wmsdelivery-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsDelivery.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsDelivery.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = WmsDelivery.objects.get()

    def test_get_wmsdelivery_list(self):
        url = reverse('wmsdelivery-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wmsdelivery(self):
        url = reverse('wmsdelivery-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = WmsDelivery.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsDelivery.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('wmsdelivery-list')
        search_key = random.choice(WmsDeliveryViewSet.search_fields)
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
