import pytest
from fastapi.testclient import TestClient

from noteit_api.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["message"] == "NoteIt API is running successfully"
    assert data["version"] == "0.1.0"