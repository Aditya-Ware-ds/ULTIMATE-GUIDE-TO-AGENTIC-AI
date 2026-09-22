"""Fixtures for the fix-the-failing-test lab: loads starter/ or solution/
(see shared/testing/lab_loader.py) and copies the checked-in sample_repo/
into a fresh temp directory per test, so the agent's file edits never touch
the repo's actual git-tracked files.
"""

from __future__ import annotations

import shutil
import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest

from shared.llm import get_client
from shared.testing import load_lab_module

LAB_DIR = Path(__file__).resolve().parent.parent
SAMPLE_REPO = LAB_DIR / "sample_repo"


@pytest.fixture
def coding_agent():
    return load_lab_module(LAB_DIR, "coding_agent")


@pytest.fixture
def client():
    return get_client("mock")


@pytest.fixture
def repo_copy() -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as tmp:
        # tmp lives outside this git repo, so a subprocess `pytest` run
        # against it never picks up this project's own pyproject.toml config.
        destination = Path(tmp) / "sample_repo"
        shutil.copytree(SAMPLE_REPO, destination)
        yield destination
