from pathlib import Path

import pytest

pytest.importorskip("dspy")

from shared.testing import load_lab_module  # noqa: E402

LAB_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE = {
    "What is the capital of France?": "Paris",
    "What is the capital of Japan?": "Tokyo",
}


@pytest.fixture
def dspy_optimizer():
    return load_lab_module(LAB_DIR, "dspy_optimizer")


@pytest.fixture
def knowledge_base() -> dict[str, str]:
    return dict(KNOWLEDGE_BASE)
