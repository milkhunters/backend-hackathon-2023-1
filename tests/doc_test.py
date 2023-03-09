import pytest
from .conftest import client


def test_docs():
    with client as init_client:
        response = init_client.get("/api/docs")
    assert response.status_code == 200


def test_redoc():
    with client as init_client:
        response = init_client.get("/api/redoc")
    assert response.status_code == 200
