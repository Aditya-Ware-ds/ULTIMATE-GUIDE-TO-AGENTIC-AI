from pathlib import Path

import pytest

from shared.llm import get_client
from shared.testing import load_lab_module

LAB_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def compacting_agent():
    return load_lab_module(LAB_DIR, "compacting_agent")


@pytest.fixture
def client():
    return get_client("mock")
