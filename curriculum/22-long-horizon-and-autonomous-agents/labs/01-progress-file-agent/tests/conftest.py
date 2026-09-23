from pathlib import Path

import pytest

from shared.llm import get_client
from shared.testing import load_lab_module

LAB_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def progress_agent():
    return load_lab_module(LAB_DIR, "progress_agent")


@pytest.fixture
def client():
    return get_client("mock")


@pytest.fixture
def progress_path(tmp_path) -> Path:
    return tmp_path / "progress.json"
