from pathlib import Path

import pytest

from shared.llm import get_client
from shared.testing import load_lab_module

LAB_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def eval_harness():
    return load_lab_module(LAB_DIR, "eval_harness")


@pytest.fixture
def client():
    return get_client("mock")
