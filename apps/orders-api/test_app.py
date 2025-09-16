from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_crud_flow():
    # create an order
    r = client.post("/orders", json={"item": "laptop", "quantity": 1})
    assert r.status_code == 201
    created = r.json()
    assert "id" in created
    oid = created["id"]

    # list orders should include created
    r = client.get("/orders")
    assert r.status_code == 200
    orders = r.json()
    assert any(o["id"] == oid for o in orders)

    # get by id
    r = client.get(f"/orders/{oid}")
    assert r.status_code == 200
    assert r.json()["item"] == "laptop"

    # delete
    r = client.delete(f"/orders/{oid}")
    assert r.status_code == 204

    # get after delete should 404
    r = client.get(f"/orders/{oid}")
    assert r.status_code == 404
