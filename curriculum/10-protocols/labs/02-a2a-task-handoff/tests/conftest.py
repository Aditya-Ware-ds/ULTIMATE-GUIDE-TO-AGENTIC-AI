from pathlib import Path

import pytest

from shared.testing import load_lab_module

LAB_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def a2a():
    return load_lab_module(LAB_DIR, "a2a")
