import random
import secrets
import string

import pytest
from ...conftest import client


def generate_valid_username() -> str:
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4, 20))


def generate_valid_password() -> str:
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8, 26))


def get_register_data(init_client) -> dict:
    reg_data = {
        "username": "strinfgg",
        "email": "some@mail.com",
        "password": "wdfdeg43fewf"
    }
    response = init_client.post(
        "/api/v1/auth/signIn",
        json=dict(
            username=reg_data["username"],
            password=reg_data["password"]
        )
    )

    if response.status_code == 404:
        reg_response = init_client.put(
            "/api/v1/auth/signUp",
            json=reg_data
        )
        if reg_response.status_code != 201:
            raise Exception("Can't create user")

        response = init_client.post(
            "/api/v1/auth/signIn",
            json=dict(
                username=reg_data["username"],
                password=reg_data["password"]
            )
        )
        assert response.status_code == 200

    reg_data.update(
        dict(
            access_token=response.cookies["access_token"],
            refresh_token=response.cookies["refresh_token"],
            session_id=response.cookies["session_id"]
        )
    )
    return reg_data


def register_user(init_client) -> dict:
    # reg new user
    user_name = generate_valid_username()
    password = generate_valid_password()

    response = init_client.put(
        "/api/v1/auth/signUp",
        json=dict(
            username=user_name,
            email=f"{user_name}@mail.com",
            password=password
        )
    )
    assert response.status_code == 201

    # sign in
    sign_response = init_client.post(
        "/api/v1/auth/signIn",
        json=dict(
            username=user_name,
            password=password
        )
    )
    assert sign_response.status_code == 200
    return dict(
        username=user_name,
        password=password,
        access_token=sign_response.cookies["access_token"],
        refresh_token=sign_response.cookies["refresh_token"],
        session_id=sign_response.cookies["session_id"]
    )


def test_signup_call_bad_data():
    with client as init_client:
        response = init_client.put("/api/v1/auth/signUp")
    assert response.status_code == 400

    with client as init_client:
        response = init_client.put(
            "/api/v1/auth/signUp",
            json={
                "username": "string",
                "email": "string",
                "password": "string"
            }
        )
    assert response.status_code == 400


def test_signup_duplicate_uname():
    # test duplicate username
    with client as init_client:
        user_data = get_register_data(init_client)

        response = init_client.put(
            "/api/v1/auth/signUp",
            json=user_data
        )
    assert response.status_code == 409


def test_signup_reg_user():
    # test register user
    user_name = generate_valid_username()
    password = generate_valid_password()
    with client as init_client:
        response = init_client.put(
            "/api/v1/auth/signUp",
            json=dict(
                username=user_name,
                email=f"{user_name}@mail.com",
                password=password
            )
        )
    assert response.status_code == 201


def test_signup_call_with_sign():
    # test ping with signin
    with client as init_client:
        user_data = get_register_data(init_client)
        response = init_client.put(
            "/api/v1/auth/signUp",
            json=dict(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"]
            ),
            cookies=dict(
                access_token=user_data["access_token"],
                refresh_token=user_data["refresh_token"],
                session_id=user_data["session_id"]
            )
        )
    assert response.status_code == 403


def test_signin():
    # test sign in
    with client as init_client:
        user_data = get_register_data(init_client)
        response = init_client.post(
            "/api/v1/auth/signIn",
            json=dict(
                username=user_data["username"],
                password=user_data["password"]
            ),
            cookies=dict()
        )
    assert response.status_code == 200


def test_signin_with_sign():
    # test ping with signin
    with client as init_client:
        user_data = get_register_data(init_client)
        response = init_client.post(
            "/api/v1/auth/signIn",
            json=dict(
                username=user_data["username"],
                password=user_data["password"]
            ),
            cookies=dict(
                access_token=user_data["access_token"],
                refresh_token=user_data["refresh_token"],
                session_id=user_data["session_id"]
            )
        )
    assert response.status_code == 403


def test_logout():
    # test logout
    with client as init_client:
        user_data = get_register_data(init_client)
        response = init_client.post(
            "/api/v1/auth/logout",
            cookies=dict(
                access_token=user_data["access_token"],
                refresh_token=user_data["refresh_token"],
                session_id=user_data["session_id"]
            )
        )
        assert response.status_code == 204


def test_refresh_tokens():
    # test logout
    with client as init_client:
        user_data = get_register_data(init_client)
        response = init_client.post(
            "/api/v1/auth/refresh_tokens",
            cookies=dict(
                access_token=user_data["access_token"],
                refresh_token=user_data["refresh_token"],
                session_id=user_data["session_id"]
            )
        )
        assert response.status_code == 204
