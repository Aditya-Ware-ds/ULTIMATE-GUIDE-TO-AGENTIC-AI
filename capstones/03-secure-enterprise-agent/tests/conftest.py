from pathlib import Path

import pytest

from shared.llm import get_client
from shared.testing import load_lab_module

CAPSTONE_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def secure_agent():
    return load_lab_module(CAPSTONE_DIR, "secure_agent")


@pytest.fixture
def mcp_server_module():
    return load_lab_module(CAPSTONE_DIR, "mcp_server")


@pytest.fixture
def client():
    return get_client("mock")


@pytest.fixture
def checkpoint_path(tmp_path) -> Path:
    return tmp_path / "checkpoint.json"


@pytest.fixture
def capstone_dir() -> Path:
    return CAPSTONE_DIR
