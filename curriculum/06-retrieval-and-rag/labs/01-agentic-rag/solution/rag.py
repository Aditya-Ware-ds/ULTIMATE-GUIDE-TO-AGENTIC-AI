"""Lab 06.01: agentic RAG over a small document set -- reference solution.
See ../README.md.
"""

from __future__ import annotations

import hashlib
import math
from collections import Counter
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


def build_index(documents: dict[str, str]) -> list[tuple[str, list[float]]]:
    index: list[tuple[str, list[float]]] = []
    for text in documents.values():
        for chunk in chunk_text(text):
            index.append((chunk, toy_embed(chunk)))
    return index


def hybrid_search(
    query: str,
    index: list[tuple[str, list[float]]],
    top_k: int = 3,
    alpha: float = 0.5,
) -> list[str]:
    query_vector = toy_embed(query)
    scored = [
        (
            hybrid_score(cosine_similarity(query_vector, embedding), keyword_score(query, chunk)),
            chunk,
        )
        for chunk, embedding in index
    ]
    scored.sort(key=lambda pair: -pair[0])
    return [chunk for _, chunk in scored[:top_k]]


SEARCH_TOOL = ToolDefinition(
    name="search_documents",
    description=(
        "Search the document collection for relevant passages. Call it again "
        "with a refined query if the first results aren't sufficient."
    ),
    parameters={
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
    },
)


def dispatch(tool_call: ToolCall, index: list[tuple[str, list[float]]]) -> ToolResult:
    if tool_call.name != "search_documents":
        return ToolResult(
            tool_call_id=tool_call.id,
            content=f"Unknown tool: {tool_call.name}",
            is_error=True,
        )
    try:
        results = hybrid_search(tool_call.arguments["query"], index)
        content = "\n---\n".join(results) if results else "No relevant passages found."
        return ToolResult(tool_call_id=tool_call.id, content=content)
    except Exception as exc:
        return ToolResult(tool_call_id=tool_call.id, content=f"Search failed: {exc}", is_error=True)


_SYSTEM_PROMPT = (
    "Answer questions using the search_documents tool. You may call it more than "
    "once with a refined query if the first results don't fully answer the question."
)


async def run_agentic_rag(
    client: LLMClient,
    index: list[tuple[str, list[float]]],
    user_input: str,
    max_steps: int = 5,
) -> str:
    messages: list[Message] = [
        Message(role=Role.SYSTEM, content=_SYSTEM_PROMPT),
        Message(role=Role.USER, content=user_input),
    ]
    for _ in range(max_steps):
        response = await client.complete(messages, tools=[SEARCH_TOOL])
        if not response.message.tool_calls:
            return response.message.content or ""
        messages.append(response.message)
        for tool_call in response.message.tool_calls:
            result = dispatch(tool_call, index)
            messages.append(Message(role=Role.TOOL, tool_result=result))
    return f"Stopped after {max_steps} steps without reaching a final answer."
