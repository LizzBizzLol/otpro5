from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_nodes():
    response = client.get("/api/nodes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
