from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from shared.llm import get_client
from shared.testing import load_lab_module

LAB_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def service_module():
    return load_lab_module(LAB_DIR, "service")


@pytest.fixture
def mock_client():
    return get_client("mock")


@pytest.fixture
def test_client(service_module, mock_client):
    service_module.app.dependency_overrides[service_module.get_llm_client] = lambda: mock_client
    with TestClient(service_module.app) as client:
        yield client
    service_module.app.dependency_overrides.clear()
