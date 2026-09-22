from pathlib import Path

import pytest

from shared.testing import load_lab_module

LAB_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def visualizer():
    return load_lab_module(LAB_DIR, "visualizer")
