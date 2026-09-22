import os
from pathlib import Path

import pytest

from shared.testing import load_lab_module

LAB_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def skill_validator():
    return load_lab_module(LAB_DIR, "skill_validator")


@pytest.fixture
def calculator_skill_dir():
    target = os.environ.get("LAB_TARGET", "solution")
    return LAB_DIR / target / "calculator"
