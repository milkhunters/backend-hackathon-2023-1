from ...conftest import client


def test_version():
    with client as init_client:
        response = init_client.get("/api/v1/version")
        assert response.status_code == 200
        assert response.json().get("version") is not None


def test_test_redis():
    with client as init_client:
        response = init_client.get("/api/v1/test_redis")
        assert response.status_code == 200
        assert response.json() == {"Redis": True}
