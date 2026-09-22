"""Project 01: research assistant with citations. See ../README.md for the
full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest projects/01-research-assistant/tests
"""

from __future__ import annotations

import hashlib  # noqa: F401 -- used once you implement toy_embed below
import math  # noqa: F401 -- used once you implement cosine_similarity below
import re  # noqa: F401 -- used once you implement extract_citations below
from collections import Counter  # noqa: F401 -- used once you implement toy_embed below
from dataclasses import dataclass, field
from pathlib import Path

from shared.llm import (  # noqa: F401 -- used in run_research_assistant below
    LLMClient,  # noqa: F401 -- used in run_research_assistant below
    Message,
    Role,
)
from shared.llm.types import ToolCall, ToolDefinition, ToolResult


def load_documents(documents_dir: Path) -> dict[str, str]:
    """TODO: implement (see Module 06's lab -- same contract)."""
    raise NotImplementedError


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    """TODO: implement (see Module 06's lab -- same contract)."""
    raise NotImplementedError


def toy_embed(text: str, dimensions: int = 64) -> list[float]:
    """TODO: implement (see Module 06's lab -- same contract, hashlib not hash())."""
    raise NotImplementedError


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """TODO: implement (see Module 06's lab -- same contract)."""
    raise NotImplementedError


def keyword_score(query: str, chunk: str) -> float:
    """TODO: implement (see Module 06's lab -- same contract)."""
    raise NotImplementedError


def hybrid_score(cosine_sim: float, keyword_sim: float, alpha: float = 0.5) -> float:
    """TODO: implement (see Module 06's lab -- same contract)."""
    raise NotImplementedError


def build_index(documents: dict[str, str]) -> list[tuple[str, str, list[float]]]:
    """Return (source_name, chunk_text, embedding) triples -- note the extra
    source_name field versus Module 06's (chunk_text, embedding) pairs.

    TODO: implement this.
    """
    raise NotImplementedError


def hybrid_search(
    query: str,
    index: list[tuple[str, str, list[float]]],
    top_k: int = 3,
    alpha: float = 0.5,
) -> list[tuple[str, str]]:
    """Return (source_name, chunk_text) pairs, highest hybrid_score first.

    TODO: implement this.
    """
    raise NotImplementedError


# TODO: define SEARCH_TOOL (a ToolDefinition for "search_documents").
SEARCH_TOOL: ToolDefinition | None = None


def dispatch(tool_call: ToolCall, index: list[tuple[str, str, list[float]]]) -> ToolResult:
    """Call hybrid_search; format each result as "[{source_name}]: {chunk_text}"
    so the model sees the source name it should cite. Never raise.

    TODO: implement this.
    """
    raise NotImplementedError


def extract_citations(answer: str) -> list[str]:
    """Return every [source_name]-shaped bracketed tag found in `answer`.

    TODO: implement this using re.findall(r"\\[([\\w.\\-]+)\\]", answer).
    """
    raise NotImplementedError


def verify_citations(answer: str, valid_sources: set[str]) -> list[str]:
    """Return the citations in `answer` that are NOT in `valid_sources`.

    TODO: implement this.
    """
    raise NotImplementedError


@dataclass
class ResearchAnswer:
    text: str
    citations: list[str] = field(default_factory=list)
    unverified_citations: list[str] = field(default_factory=list)


async def run_research_assistant(
    client: LLMClient,
    index: list[tuple[str, str, list[float]]],
    valid_sources: set[str],
    user_input: str,
    max_steps: int = 5,
) -> ResearchAnswer:
    """The agent loop (same shape as Modules 03-06), returning a ResearchAnswer
    with citations extracted and verified once a final text answer is reached.

    TODO: implement this.
    """
    raise NotImplementedError
