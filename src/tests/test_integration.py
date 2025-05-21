# tests/test_integration_docker.py
import os
import time
import pytest
import requests

from api_sdk.client import APIClient
from api_sdk.models import FlModel

# Base URL will be provided by the CI workflow
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000/api")

TOKEN = os.getenv("SDK_TEST_TOKEN")

@pytest.fixture(scope="session")
def api_client():
    return APIClient(API_BASE, token=TOKEN)

def wait_for_api(url, timeout=60):
    """Poll until the API responds (status 200 or 401)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(url + "/models/")
            if r.status_code in (200, 401):
                return
        except requests.ConnectionError:
            pass
        time.sleep(2)
    pytest.skip(f"API not reachable at {url} after {timeout}s")

def test_list_models_against_server(api_client):
    # Wait until the server is up
    wait_for_api(API_BASE)

    # Perform the SDK call
    models = api_client.list_models()
    assert isinstance(models, list)

    # If you seeded some FlModels via docker-compose, assert they exist:
    # e.g. expect at least one pre-seeded model named "TestModel"
    names = [m.name for m in models]
    assert "TestModel" in names
