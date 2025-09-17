import requests

def test_health():
    r = requests.get("http://localhost:8081/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
