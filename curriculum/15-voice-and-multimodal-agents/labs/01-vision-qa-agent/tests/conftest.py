from pathlib import Path

import pytest

from shared.llm import get_client
from shared.testing import load_lab_module

LAB_DIR = Path(__file__).resolve().parent.parent
IMAGE_PATH = LAB_DIR / "images" / "red_square_on_blue.png"


@pytest.fixture
def vision_agent():
    return load_lab_module(LAB_DIR, "vision_agent")


@pytest.fixture
def client():
    return get_client("mock")


@pytest.fixture
def image_path() -> Path:
    return IMAGE_PATH
