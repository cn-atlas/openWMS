import pytest
from account.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

import logging

logger = logging.getLogger(__name__)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client):
    user, created = User.objects.get_or_create(username='zk', password="zkjy2023")
    refresh = RefreshToken.for_user(user)
    logger.debug(f'token: {refresh}')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh}')
    return api_client
