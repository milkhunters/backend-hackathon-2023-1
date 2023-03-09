import pytest

from .auth_router_test import get_register_data, generate_valid_username, generate_valid_password, register_user
from ...conftest import client


def test_current_user_unsign():
    with client as init_client:
        response = init_client.get("/api/v1/user/current")
    assert response.status_code == 403


def test_current_user_sign():
    with client as init_client:
        user_data = get_register_data(init_client)
        response = init_client.get(
            "/api/v1/user/current",
            cookies=dict(
                session_id=user_data["session_id"],
                access_token=user_data["access_token"],
                refresh_token=user_data["refresh_token"]
            )
        )
    assert response.status_code == 200


def test_select_wrong_user_uuid():
    with client as init_client:
        response = init_client.get("/api/v1/user/9223372036854775807")
    assert response.status_code == 400


def test_unsign_update_user():
    with client as init_client:
        response = init_client.post("/api/v1/user/update")
    assert response.status_code == 400


def test_update_user_sign():
    # test update user sign
    with client as init_client:
        user_data = register_user(init_client)
        response = init_client.post(
            "/api/v1/user/update",
            json={"username": generate_valid_username()},
            cookies=dict(
                session_id=user_data["session_id"],
                access_token=user_data["access_token"],
                refresh_token=user_data["refresh_token"]
            )
        )
    assert response.status_code == 204


def test_delete_user_unsign():
    with client as init_client:
        response = init_client.delete("/api/v1/user/delete")
    assert response.status_code == 403


def test_delete_user_sign():
    # test delete user sign
    with client as init_client:
        user_data = register_user(init_client)
        response = init_client.delete(
            "/api/v1/user/delete",
            cookies=dict(
                session_id=user_data["session_id"],
                access_token=user_data["access_token"],
                refresh_token=user_data["refresh_token"]
            )
        )
    assert response.status_code == 204
