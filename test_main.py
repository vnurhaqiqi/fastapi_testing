from fastapi.testclient import TestClient

from .main import *

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_get_product_by_id_bad_token():
    response = client.get("/products/1", headers={"x-token": "this_bad_token"})
    assert response.status_code == 400
    assert response.json() == {"detail": "invalid token"}


def test_get_product_by_id():
    response = client.get("/products/1", headers={"x-token": "this_is_secret"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Monitor",
        "price": 200,
        "qty": 10
    }


def test_get_product_by_id_not_found():
    response = client.get(
        "/products/100", headers={"x-token": "this_is_secret"})
    assert response.status_code == 404
    assert response.json() == {"detail": "product not found"}


def test_create_product():
    response = client.post("/products/", headers={"x-token": "this_is_secret"}, json={
        "title": "Test",
        "price": 20,
        "qty": 2
    })
    assert response.status_code == 200
    assert response.json() == {
        "id": len(fake_db),
        "title": "Test",
        "price": 20,
        "qty": 2
    }
