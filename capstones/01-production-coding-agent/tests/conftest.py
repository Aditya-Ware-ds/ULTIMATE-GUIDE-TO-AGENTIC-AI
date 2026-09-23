"""Fixtures for Capstone 1: loads starter/ or solution/ (see
shared/testing/lab_loader.py) and copies a sample_repo/ subdirectory into a
fresh temp directory per test, so the agent's edits never touch the repo's
actual git-tracked files (same reasoning as Module 13's repo_copy fixture).
"""

from __future__ import annotations

import shutil
import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest

from shared.llm import get_client
from shared.testing import load_lab_module

CAPSTONE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_REPO_ROOT = CAPSTONE_DIR / "sample_repo"


@pytest.fixture
def coding_agent():
    return load_lab_module(CAPSTONE_DIR, "coding_agent")


@pytest.fixture
def eval_harness():
    return load_lab_module(CAPSTONE_DIR, "eval_harness")


@pytest.fixture
def client():
    return get_client("mock")


@pytest.fixture
def sample_repo_root() -> Path:
    return SAMPLE_REPO_ROOT


@pytest.fixture
def calculator_repo_copy() -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as tmp:
        destination = Path(tmp) / "calculator"
        shutil.copytree(SAMPLE_REPO_ROOT / "calculator", destination)
        yield destination
