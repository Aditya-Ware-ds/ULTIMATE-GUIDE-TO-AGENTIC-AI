from pathlib import Path

import pytest

from shared.llm import get_client
from shared.testing import load_lab_module
from shared.tracing import clear_exported_spans

LAB_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def traced_agent():
    return load_lab_module(LAB_DIR, "traced_agent")


@pytest.fixture
def client():
    return get_client("mock")


@pytest.fixture(autouse=True)
def _clear_spans():
    clear_exported_spans()
    yield
    clear_exported_spans()
