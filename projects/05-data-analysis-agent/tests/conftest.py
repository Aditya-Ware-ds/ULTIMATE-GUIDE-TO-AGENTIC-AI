"""Fixtures for the data-analysis-agent project: loads starter/ or solution/
(see shared/testing/lab_loader.py) and copies the checked-in dataset/ into a
fresh temp directory per test, so the agent's sandboxed code never touches
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
DATASET = LAB_DIR / "dataset"


@pytest.fixture
def data_agent():
    return load_lab_module(LAB_DIR, "data_agent")


@pytest.fixture
def client():
    return get_client("mock")


@pytest.fixture
def dataset_dir() -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as tmp:
        destination = Path(tmp) / "dataset"
        shutil.copytree(DATASET, destination)
        yield destination
