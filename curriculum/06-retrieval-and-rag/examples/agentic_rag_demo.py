"""Run: uv run python curriculum/06-retrieval-and-rag/examples/agentic_rag_demo.py

Shows retrieval as a tool inside the Module 04 agent loop, including a second,
refined search call. See lessons/03-agentic-rag.md. No API key needed.
"""

from __future__ import annotations

import asyncio

from shared.llm import Message, Role, get_client
from shared.llm.types import ToolDefinition, ToolResult

DOCUMENTS = [
    "The refund policy allows returns within 30 days of purchase with a receipt.",
    "Shipping typically takes 3-5 business days within the country.",
    "International orders may take 2-3 weeks depending on customs.",
]

SEARCH_DOCUMENTS = ToolDefinition(
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


def naive_search(query: str) -> str:
    query_words = set(query.lower().split())
    scored = [(len(query_words & set(doc.lower().split())), doc) for doc in DOCUMENTS]
    scored.sort(key=lambda pair: -pair[0])
    return scored[0][1] if scored[0][0] > 0 else "No relevant passage found."


async def main() -> None:
    client = get_client("mock")
    client.provider.add_tool_call("search_documents", {"query": "refund policy"})
    client.provider.add_tool_call("search_documents", {"query": "international shipping time"})
    client.provider.add_text(
        "Refunds are allowed within 30 days, and international shipping takes 2-3 weeks."
    )

    messages = [
        Message(role=Role.SYSTEM, content="Answer using search_documents."),
        Message(
            role=Role.USER,
            content="What's the refund policy, and how long does international shipping take?",
        ),
    ]

    for step in range(5):
        response = await client.complete(messages, tools=[SEARCH_DOCUMENTS])
        if not response.message.tool_calls:
            print(f"Final answer: {response.message.content}")
            break
        messages.append(response.message)
        for call in response.message.tool_calls:
            query = call.arguments["query"]
            result = naive_search(query)
            print(f"step {step + 1}: search({query!r}) -> {result!r}")
            messages.append(
                Message(
                    role=Role.TOOL, tool_result=ToolResult(tool_call_id=call.id, content=result)
                )
            )


if __name__ == "__main__":
    asyncio.run(main())
