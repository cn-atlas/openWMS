import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User
from rest_framework.test import APIClient
from api.views.WMSViewSet import WmsInventoryMovementViewSet
from api.filters.WMSFilter import WmsInventoryMovementFilter
from api.tests.WMSTests import common
from WMS.models.movement import WmsInventoryMovement
import logging

logger = logging.getLogger(__name__)


class WmsInventoryMovementTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.client.force_authenticate(self.user)
        self.test_data = {'is_show': True, 'create_time': '2011-04-25 00:00:00', 'edit_time': '1979-12-30 00:00:00',
                          'creator': None, 'editor': None, 'is_checked': True, 'check_time': '2016-07-30 00:00:00',
                          'check_user': None, 'check_note': '那个怎么.', 'number': '2srf0ysk9w', 'source_rack': None,
                          'target_rack': None, 'status': 1, 'remark': '威望不是一点.'}
        # is_checked 为 False 的时候 status 必须是 3
        self.update_data = {'is_checked': False, 'check_note': '阅读控制作品一下.', 'number': 'JiIbYZzgJq', 'status': 3,
                            'remark': '全部很多重要.'}

        url = reverse('wmsinventorymovement-list')
        # logger.debug(self.client)
        response = self.client.post(url, self.test_data, format='json')
        # logger.debug(url, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WmsInventoryMovement.objects.count(), 1)
        # update_data 可以避开 datetime field
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsInventoryMovement.objects.get(), key)
        self.assertEqual(value, self.test_data.get(key))
        self.obj = WmsInventoryMovement.objects.get()

    def test_get_wmsinventorymovement_list(self):
        url = reverse('wmsinventorymovement-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_wmsinventorymovement(self):
        url = reverse('wmsinventorymovement-detail', args=[self.obj.id])
        response = self.client.patch(url, self.update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj = WmsInventoryMovement.objects.get()
        key = random.choice(list(self.update_data.keys()))
        value = getattr(WmsInventoryMovement.objects.get(), key)
        self.assertEqual(value, self.update_data.get(key))

    def test_search(self):
        url = reverse('wmsinventorymovement-list')
        search_key = random.choice(WmsInventoryMovementViewSet.search_fields)
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
