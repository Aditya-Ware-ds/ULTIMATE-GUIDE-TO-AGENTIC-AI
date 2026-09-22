from pathlib import Path

import pytest

pytest.importorskip("crewai")

from shared.testing import load_lab_module  # noqa: E402

LAB_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def agent_module():
    return load_lab_module(LAB_DIR, "agent")
