"""Lab 06.01: agentic RAG over a small document set. See ../README.md for the
full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/06-retrieval-and-rag/labs/01-agentic-rag/tests
"""

from __future__ import annotations

import hashlib  # noqa: F401 -- used once you implement toy_embed below
import math  # noqa: F401 -- used once you implement cosine_similarity below
from collections import Counter  # noqa: F401 -- used once you implement toy_embed below
from pathlib import Path

from shared.llm import LLMClient, Message, Role  # noqa: F401 -- used in run_agentic_rag below
from shared.llm.types import ToolCall, ToolDefinition, ToolResult


def load_documents(documents_dir: Path) -> dict[str, str]:
    """Read every .txt file in documents_dir, keyed by filename.

    TODO: implement this.
    """
    raise NotImplementedError


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    """Fixed-size chunking with overlap.

    TODO: implement this (see lessons/01-chunking-and-embeddings.md).
    """
    raise NotImplementedError


def toy_embed(text: str, dimensions: int = 64) -> list[float]:
    """A deterministic hash-based bag-of-trigrams vector. Use hashlib.md5, NOT
    Python's built-in hash() (which is randomized per-process).

    TODO: implement this.
    """
    raise NotImplementedError


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """TODO: implement this. Return 0.0 if either vector has zero magnitude."""
    raise NotImplementedError


def keyword_score(query: str, chunk: str) -> float:
    """Fraction of query words present in the chunk.

    TODO: implement this (see lessons/02-hybrid-search-and-ranking.md).
    """
    raise NotImplementedError


def hybrid_score(cosine_sim: float, keyword_sim: float, alpha: float = 0.5) -> float:
    """TODO: implement this (weighted combination)."""
    raise NotImplementedError


def build_index(documents: dict[str, str]) -> list[tuple[str, list[float]]]:
    """Chunk every document, embed every chunk, return (chunk_text, embedding) pairs.

    TODO: implement this.
    """
    raise NotImplementedError


def hybrid_search(
    query: str,
    index: list[tuple[str, list[float]]],
    top_k: int = 3,
    alpha: float = 0.5,
) -> list[str]:
    """Return the top_k chunk texts ranked by hybrid_score, highest first.

    TODO: implement this.
    """
    raise NotImplementedError


# TODO: define SEARCH_TOOL (a ToolDefinition for "search_documents").
SEARCH_TOOL: ToolDefinition | None = None


def dispatch(tool_call: ToolCall, index: list[tuple[str, list[float]]]) -> ToolResult:
    """Call hybrid_search and join results into ToolResult.content. Never raise.

    TODO: implement this.
    """
    raise NotImplementedError


async def run_agentic_rag(
    client: LLMClient,
    index: list[tuple[str, list[float]]],
    user_input: str,
    max_steps: int = 5,
) -> str:
    """Agent loop with search_documents as a tool.

    TODO: implement this (same loop shape as Modules 03-05, with search as the tool).
    """
    raise NotImplementedError
