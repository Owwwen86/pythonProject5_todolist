import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from tests.factories import BoardFactory, UserFactory, CategoryFactory


pytest_plugins = 'tests.factories'
register(BoardFactory)
register(UserFactory)
register(CategoryFactory)


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture()
def auth_client(client, user) -> APIClient:
    client.force_login(user)
    return client
