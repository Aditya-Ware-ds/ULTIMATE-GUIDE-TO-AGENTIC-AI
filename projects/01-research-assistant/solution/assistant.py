"""Project 01: research assistant with citations -- reference solution.
See ../README.md.
"""

from __future__ import annotations

import hashlib
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from shared.llm import LLMClient, Message, Role
from shared.llm.types import ToolCall, ToolDefinition, ToolResult


def load_documents(documents_dir: Path) -> dict[str, str]:
    return {path.name: path.read_text() for path in sorted(documents_dir.glob("*.txt"))}


def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def toy_embed(text: str, dimensions: int = 64) -> list[float]:
    vector = [0.0] * dimensions
    text = text.lower()
    trigrams = Counter(text[i : i + 3] for i in range(len(text) - 2))
    for trigram, count in trigrams.items():
        bucket = int(hashlib.md5(trigram.encode()).hexdigest(), 16) % dimensions
        vector[bucket] += count
    return vector


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(y * y for y in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def keyword_score(query: str, chunk: str) -> float:
    query_words = set(query.lower().split())
    chunk_words = set(chunk.lower().split())
    if not query_words:
        return 0.0
    return len(query_words & chunk_words) / len(query_words)


def hybrid_score(cosine_sim: float, keyword_sim: float, alpha: float = 0.5) -> float:
    return alpha * cosine_sim + (1 - alpha) * keyword_sim


def build_index(documents: dict[str, str]) -> list[tuple[str, str, list[float]]]:
    index: list[tuple[str, str, list[float]]] = []
    for source_name, text in documents.items():
        for chunk in chunk_text(text):
            index.append((source_name, chunk, toy_embed(chunk)))
    return index


def hybrid_search(
    query: str,
    index: list[tuple[str, str, list[float]]],
    top_k: int = 3,
    alpha: float = 0.5,
) -> list[tuple[str, str]]:
    query_vector = toy_embed(query)
    scored = [
        (
            hybrid_score(cosine_similarity(query_vector, embedding), keyword_score(query, chunk)),
            source_name,
            chunk,
        )
        for source_name, chunk, embedding in index
    ]
    scored.sort(key=lambda triple: -triple[0])
    return [(source_name, chunk) for _, source_name, chunk in scored[:top_k]]


SEARCH_TOOL = ToolDefinition(
    name="search_documents",
    description=(
        "Search the document collection for relevant passages. Results are "
        "labeled with their source, like '[apollo-program.txt]: ...'. When you "
        "give your final answer, cite the bracketed source name for each fact. "
        "Call this tool again with a refined query if needed."
    ),
    parameters={
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
    },
)


def dispatch(tool_call: ToolCall, index: list[tuple[str, str, list[float]]]) -> ToolResult:
    if tool_call.name != "search_documents":
        return ToolResult(
            tool_call_id=tool_call.id,
            content=f"Unknown tool: {tool_call.name}",
            is_error=True,
        )
    try:
        results = hybrid_search(tool_call.arguments["query"], index)
        if not results:
            content = "No relevant passages found."
        else:
            content = "\n---\n".join(f"[{source}]: {chunk}" for source, chunk in results)
        return ToolResult(tool_call_id=tool_call.id, content=content)
    except Exception as exc:
        return ToolResult(tool_call_id=tool_call.id, content=f"Search failed: {exc}", is_error=True)


_CITATION_RE = re.compile(r"\[([\w.\-]+)\]")


def extract_citations(answer: str) -> list[str]:
    return _CITATION_RE.findall(answer)


def verify_citations(answer: str, valid_sources: set[str]) -> list[str]:
    return [c for c in extract_citations(answer) if c not in valid_sources]


@dataclass
class ResearchAnswer:
    text: str
    citations: list[str] = field(default_factory=list)
    unverified_citations: list[str] = field(default_factory=list)


_SYSTEM_PROMPT = (
    "You are a research assistant. Answer using the search_documents tool, and "
    "cite the bracketed source name for each fact in your final answer, e.g. "
    "'Apollo 11 landed in 1969 [apollo-program.txt].' You may search more than "
    "once with a refined query."
)


async def run_research_assistant(
    client: LLMClient,
    index: list[tuple[str, str, list[float]]],
    valid_sources: set[str],
    user_input: str,
    max_steps: int = 5,
) -> ResearchAnswer:
    messages: list[Message] = [
        Message(role=Role.SYSTEM, content=_SYSTEM_PROMPT),
        Message(role=Role.USER, content=user_input),
    ]
    for _ in range(max_steps):
        response = await client.complete(messages, tools=[SEARCH_TOOL])
        if not response.message.tool_calls:
            text = response.message.content or ""
            citations = extract_citations(text)
            unverified = verify_citations(text, valid_sources)
            return ResearchAnswer(text=text, citations=citations, unverified_citations=unverified)
        messages.append(response.message)
        for tool_call in response.message.tool_calls:
            result = dispatch(tool_call, index)
            messages.append(Message(role=Role.TOOL, tool_result=result))
    text = f"Stopped after {max_steps} steps without reaching a final answer."
    return ResearchAnswer(text=text)
