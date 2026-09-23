from pathlib import Path

import pytest

from shared.llm import get_client
from shared.testing import load_lab_module
from shared.tracing import clear_exported_spans

CAPSTONE_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def research_pipeline():
    return load_lab_module(CAPSTONE_DIR, "research_pipeline")


@pytest.fixture
def eval_suite():
    return load_lab_module(CAPSTONE_DIR, "eval_suite")


@pytest.fixture
def client():
    return get_client("mock")


@pytest.fixture(autouse=True)
def _clear_spans():
    clear_exported_spans()
    yield
    clear_exported_spans()
