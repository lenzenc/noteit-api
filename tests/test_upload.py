from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from noteit_api.main import app

client = TestClient(app)


def test_upload_valid_image():
    # Create a simple test image (1x1 pixel PNG)
    test_image_data = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01'
        b'\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    
    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.png", BytesIO(test_image_data), "image/png")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "File uploaded successfully"
    assert data["filename"] == "test.png"
    assert "file_id" in data
    assert data["file_size"] == len(test_image_data)
    assert data["content_type"] == "image/png"
    assert "imgproxy_url" in data


def test_upload_invalid_content_type():
    test_file_data = b"not an image"
    
    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.txt", BytesIO(test_file_data), "text/plain")}
    )
    
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]


def test_upload_empty_file():
    response = client.post(
        "/api/v1/upload",
        files={"file": ("empty.png", BytesIO(b""), "image/png")}
    )
    
    assert response.status_code == 400
    assert "File is empty" in response.json()["detail"]


def test_upload_file_too_large():
    # Create a file larger than the 10MB limit
    large_data = b"x" * (11 * 1024 * 1024)  # 11MB
    
    response = client.post(
        "/api/v1/upload",
        files={"file": ("large.png", BytesIO(large_data), "image/png")}
    )
    
    assert response.status_code == 400
    assert "File too large" in response.json()["detail"]


def test_health_endpoint_still_works():
    # Ensure we didn't break the existing health endpoint
    response = client.get("/api/v1/health")
    assert response.status_code == 200