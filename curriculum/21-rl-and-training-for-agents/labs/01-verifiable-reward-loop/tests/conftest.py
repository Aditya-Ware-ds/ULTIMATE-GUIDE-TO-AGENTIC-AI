from pathlib import Path

import pytest

from shared.testing import load_lab_module

LAB_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def rlvr_loop():
    return load_lab_module(LAB_DIR, "rlvr_loop")
