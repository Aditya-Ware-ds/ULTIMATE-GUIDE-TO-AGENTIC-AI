"""Lab 10.01: MCP client calling the server's tools -- reference solution.
See ../README.md.
"""

from __future__ import annotations


async def list_available_tools(client) -> list[str]:
    tools = await client.list_tools()
    return [t.name for t in tools.tools]


async def call_calculate(client, expression: str) -> float:
    result = await client.call_tool("calculate", {"expression": expression})
    return result.structured_content["result"]


async def call_get_weather(client, city: str) -> str:
    """Raises ValueError (with the server's error text) if the tool call
    itself errors, rather than returning an ambiguous result.
    """
    result = await client.call_tool("get_weather", {"city": city})
    if result.is_error:
        error_text = result.content[0].text if result.content else "unknown error"
        raise ValueError(error_text)
    return result.content[0].text
