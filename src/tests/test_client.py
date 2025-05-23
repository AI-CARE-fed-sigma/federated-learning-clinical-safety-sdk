# tests/test_client.py
import pytest
from requests import HTTPError

from api_sdk.client import APIClient
from api_sdk.exceptions import APIError
from api_sdk.models import FlModel, LocalModel

BASE = "http://example.com/api"
TOKEN = "fake-token"

@pytest.fixture
def client():
    return APIClient(BASE, TOKEN)

def make_url(path: str) -> str:
    return f"{BASE.rstrip('/')}{path}"

def test_list_models_success(requests_mock, client):
    data = [
        {"id": 1, "name": "M1", "accuracy": 0.8, "generalisability": 0.7, "privacy": 0.6},
        {"id": 2, "name": "M2", "accuracy": 0.9, "generalisability": 0.85, "privacy": None},
    ]
    requests_mock.get(make_url("/models/"), json=data, status_code=200)

    models = client.list_models()
    assert isinstance(models, list)
    assert len(models) == 2
    assert models[0].name == "M1"
    assert models[1].privacy is None  # now privacy instead of security

def test_list_models_error_raises(requests_mock, client):
    requests_mock.get(make_url("/models/"), text="Forbidden", status_code=403)
    with pytest.raises(APIError) as exc:
        client.list_models()
    assert "APIError 403" in str(exc.value)

def test_get_model_success(requests_mock, client):
    payload = {
        "id": 42,
        "name": "Answer",
        "accuracy": 1.0,
        "generalisability": 1.0,
        "privacy": 1.0
    }
    requests_mock.get(make_url("/models/42/"), json=payload, status_code=200)

    m = client.get_model(42)
    assert isinstance(m, FlModel)
    assert m.id == 42
    assert m.name == "Answer"
    assert m.privacy == 1.0

def test_create_model_success(requests_mock, client):
    to_create = FlModel(name="New", accuracy=0.5, generalisability=0.4)
    response_payload = {
        "id": 99,
        "name": "New",
        "accuracy": 0.5,
        "generalisability": 0.4,
        "privacy": None
    }
    requests_mock.post(make_url("/models/"), json=response_payload, status_code=201)

    created = client.create_model(to_create)
    assert created.id == 99
    assert created.name == "New"
    assert created.privacy is None

def test_list_local_models_success(requests_mock, client):
    data = [
        {
            "id": 1,
            "fl_model": 42,
            "name": "LocalA",
            "privacy": 0.3,
            "leakage_chance": 0.1,
            "noise": 0.05
        },
    ]
    requests_mock.get(make_url("/models/42/locals/"), json=data, status_code=200)

    locals_ = client.list_local_models(42)
    assert len(locals_) == 1
    lm = locals_[0]
    assert isinstance(lm, LocalModel)
    assert lm.privacy == 0.3
    assert lm.leakage_chance == 0.1
    assert lm.noise == 0.05
