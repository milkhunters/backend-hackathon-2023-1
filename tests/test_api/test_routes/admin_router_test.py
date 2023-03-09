import pytest

from .auth_router_test import get_register_data, generate_valid_username, register_user
from ...conftest import client


def test_admin_get_user_unsign():
    with client as init_client:
        response = init_client.get("/api/v1/admin/get_user/e8aa329c-9d25-4866-be25-15896c2416ba")
    assert response.status_code == 403


def test_admin_update_user_unsign():
    with client as init_client:
        response = init_client.post(
            "/api/v1/admin/update_user/e8aa329c-9d25-4866-be25-15896c2416ba",
            json=dict(
                username='JKearnsl'
            )
        )
    print(response.content)
    assert response.status_code == 403
