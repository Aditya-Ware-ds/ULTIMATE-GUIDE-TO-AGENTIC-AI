"""Run: uv run python curriculum/04-agent-loop/examples/react_trace_demo.py

Shows a ReAct-style trace: reasoning text alongside each tool call, printed as
Thought/Action/Observation. See lessons/03-react-pattern.md.
"""

from __future__ import annotations

import asyncio

from shared.llm import Message, Role, get_client
from shared.llm.types import Message as MessageType
from shared.llm.types import ToolCall, ToolDefinition, ToolResult

SEARCH = ToolDefinition(
    name="search",
    description="Look up a fact.",
    parameters={
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
    },
)

KNOWLEDGE = {
    "capital of france": "Paris is the capital of France.",
    "population of paris": "Paris has a population of about 2.1 million.",
}


def fake_search(query: str) -> str:
    return KNOWLEDGE.get(query.lower(), f"No information found for {query!r}.")


async def main() -> None:
    client = get_client("mock")
    client.provider.add_response(
        MessageType(
            role=Role.ASSISTANT,
            content="I need to find the capital of France first.",
            tool_calls=[ToolCall(id="1", name="search", arguments={"query": "capital of France"})],
        )
    )
    client.provider.add_response(
        MessageType(
            role=Role.ASSISTANT,
            content="Now I need the population of Paris.",
            tool_calls=[
                ToolCall(id="2", name="search", arguments={"query": "population of Paris"})
            ],
        )
    )
    client.provider.add_text("The capital of France, Paris, has a population of about 2.1 million.")

    messages = [Message(role=Role.USER, content="What's the population of France's capital?")]

    for _ in range(5):
        response = await client.complete(messages, tools=[SEARCH])
        if not response.message.tool_calls:
            print(f"Final Answer: {response.message.content}")
            break
        if response.message.content:
            print(f"Thought: {response.message.content}")
        messages.append(response.message)
        for call in response.message.tool_calls:
            print(f"Action: search({call.arguments['query']!r})")
            observation = fake_search(call.arguments["query"])
            print(f"Observation: {observation}")
            messages.append(
                Message(
                    role=Role.TOOL,
                    tool_result=ToolResult(tool_call_id=call.id, content=observation),
                )
            )


if __name__ == "__main__":
    asyncio.run(main())
