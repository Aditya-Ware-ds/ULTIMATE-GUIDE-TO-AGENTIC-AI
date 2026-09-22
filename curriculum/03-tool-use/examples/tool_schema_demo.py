"""Run: uv run python curriculum/03-tool-use/examples/tool_schema_demo.py

Shows a well-formed ToolDefinition and how it's sent to the model, as covered in
lessons/01-tool-schemas.md. No API key needed.
"""

from __future__ import annotations

import asyncio
import json

from shared.llm import Message, Role, get_client
from shared.llm.types import ToolDefinition

GET_WEATHER = ToolDefinition(
    name="get_weather",
    description=(
        "Get the current weather for a city. Use this whenever the user asks "
        "about weather, temperature, or conditions in a specific place."
    ),
    parameters={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name, e.g. 'Paris'."},
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit. Defaults to celsius if omitted.",
            },
        },
        "required": ["city"],
    },
)


async def main() -> None:
    client = get_client("mock")
    client.provider.add_tool_call("get_weather", {"city": "Paris", "unit": "celsius"})

    messages = [Message(role=Role.USER, content="What's the weather in Paris?")]
    response = await client.complete(messages, tools=[GET_WEATHER])

    print("Model requested a tool call:")
    for call in response.message.tool_calls:
        print(f"  name: {call.name}")
        print(f"  arguments: {json.dumps(call.arguments)}")

    print("\nWhat the model actually saw as the tool's definition:")
    print(json.dumps({"name": GET_WEATHER.name, "parameters": GET_WEATHER.parameters}, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
