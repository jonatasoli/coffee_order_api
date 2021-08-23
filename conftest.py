import pytest
from fastapi.testclient import TestClient
from main import create_app as app

@pytest.fixture
def client():
    with TestClient(app()) as client:
        yield client
