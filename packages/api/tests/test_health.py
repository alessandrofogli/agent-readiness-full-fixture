from api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health() -> None:
    assert client.get("/health").json() == {"status": "ok"}


def test_ready_and_live() -> None:
    assert client.get("/ready").status_code == 200
    assert client.get("/live").status_code == 200
