from pathlib import Path

import pytest

from shared.llm import get_client
from shared.testing import load_lab_module

LAB_DIR = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = LAB_DIR / "documents"


@pytest.fixture
def rag():
    return load_lab_module(LAB_DIR, "rag")


@pytest.fixture
def client():
    return get_client("mock")


@pytest.fixture
def documents(rag):
    return rag.load_documents(DOCUMENTS_DIR)


@pytest.fixture
def index(rag, documents):
    return rag.build_index(documents)
