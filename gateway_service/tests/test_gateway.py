import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import app

# Mock environment variable
@pytest.fixture(autouse=True)
def set_env():
    with patch.dict(os.environ, {"STORAGE_SERVICES": "storage_service_1,storage_service_2"}):
        app.STORAGE_SERVICES = app.get_storage_services()
        app.service_cycle = iter(app.STORAGE_SERVICES.values())

@pytest.fixture
def client():
    return TestClient(app.app)

@patch("requests.get")
def test_check_status(mock_get, client):
    """Test /status endpoint with mocked storage services."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {
        "storage_1": "available",
        "storage_2": "available"
    }

@patch("requests.get")
def test_check_status_unavailable(mock_get, client):
    """Test /status endpoint when services are unavailable."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {
        "storage_1": "unavailable",
        "storage_2": "unavailable"
    }

@patch("requests.get")
def test_get_data(mock_get, client):
    """Test /data endpoint with a successful storage response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}
    mock_get.return_value = mock_response
    
    response = client.get("/data")
    assert response.status_code == 200
    assert response.json() == {"key": "value"}

@patch("requests.get")
def test_get_data_all_unavailable(mock_get, client):
    """Test /data endpoint when all storage services are unavailable."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    
    response = client.get("/data")
    assert response.status_code == 503
    assert response.json()["detail"] == "No storage services available"
