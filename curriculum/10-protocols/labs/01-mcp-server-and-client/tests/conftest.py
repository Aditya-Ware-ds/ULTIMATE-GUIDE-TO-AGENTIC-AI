from pathlib import Path

import pytest

from shared.testing import load_lab_module

LAB_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def server_module():
    return load_lab_module(LAB_DIR, "server")


@pytest.fixture
def client_module():
    return load_lab_module(LAB_DIR, "client")
