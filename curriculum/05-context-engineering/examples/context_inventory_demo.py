"""Run: uv run python curriculum/05-context-engineering/examples/context_inventory_demo.py

Breaks down exactly what's competing for space in one agent call's context, with
real token counts via tiktoken. See lessons/01-what-goes-in-context.md.
"""

from __future__ import annotations

import json

import tiktoken

from shared.llm.types import Message, Role, ToolDefinition

SYSTEM_PROMPT = "You are a helpful research assistant. Be concise and cite sources."

TOOLS = [
    ToolDefinition(
        name="search",
        description="Search the web for information on a topic.",
        parameters={
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    ),
    ToolDefinition(
        name="fetch_page",
        description="Fetch and read the full text content of a specific URL.",
        parameters={
            "type": "object",
            "properties": {"url": {"type": "string"}},
            "required": ["url"],
        },
    ),
]

HISTORY = [
    Message(role=Role.USER, content="What are the latest developments in fusion energy?"),
    Message(role=Role.ASSISTANT, content="Let me search for recent fusion energy news."),
]

RETRIEVED_DOCUMENT = "Fusion energy research has seen significant progress... " * 20


def count_tokens(text: str) -> int:
    encoding = tiktoken.get_encoding("o200k_base")
    return len(encoding.encode(text))


def main() -> None:
    system_tokens = count_tokens(SYSTEM_PROMPT)
    tools_tokens = count_tokens(
        json.dumps([{"name": t.name, "parameters": t.parameters} for t in TOOLS])
    )
    history_tokens = sum(count_tokens(m.content or "") for m in HISTORY)
    document_tokens = count_tokens(RETRIEVED_DOCUMENT)

    print("Context inventory for one agent call:")
    print(f"  system prompt:       {system_tokens:>5} tokens")
    print(f"  tool definitions:    {tools_tokens:>5} tokens ({len(TOOLS)} tools)")
    print(f"  conversation history:{history_tokens:>5} tokens ({len(HISTORY)} messages)")
    print(f"  retrieved document:  {document_tokens:>5} tokens")
    total = system_tokens + tools_tokens + history_tokens + document_tokens
    print(f"  {'-' * 30}")
    print(f"  total:               {total:>5} tokens")


if __name__ == "__main__":
    main()
