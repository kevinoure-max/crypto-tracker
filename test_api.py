from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_get_coin_valid():
    response = client.get("/coins/bitcoin?days=7")
    assert response.status_code == 200
    data = response.json()
    assert "current_price" in data
    assert "high" in data
    assert data["coin"] == "bitcoin"


def test_get_coin_invalid():
    response = client.get("/coins/bicoin?days=7")
    assert response.status_code == 404


def test_get_coin_invalid_days():
    response = client.get("/coins/bitcoin?days=0")
    assert response.status_code == 400
