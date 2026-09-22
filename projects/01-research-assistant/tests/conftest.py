from pathlib import Path

import pytest

from shared.llm import get_client
from shared.testing import load_lab_module

PROJECT_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = PROJECT_DIR / "documents"


@pytest.fixture
def assistant():
    return load_lab_module(PROJECT_DIR, "assistant")


@pytest.fixture
def client():
    return get_client("mock")


@pytest.fixture
def documents(assistant):
    return assistant.load_documents(DOCUMENTS_DIR)


@pytest.fixture
def valid_sources(documents):
    return set(documents.keys())


@pytest.fixture
def index(assistant, documents):
    return assistant.build_index(documents)
