"""Lab 10.01: MCP client calling the server's tools.
See ../README.md for the full spec.
"""

from __future__ import annotations


async def list_available_tools(client) -> list[str]:
    """Return the names of every tool the connected server exposes.

    TODO: implement this.
    """
    raise NotImplementedError


async def call_calculate(client, expression: str) -> float:
    """Call the server's calculate tool and return the numeric result.

    TODO: implement this. Prefer result.structured_content["result"].
    """
    raise NotImplementedError


async def call_get_weather(client, city: str) -> str:
    """Call the server's get_weather tool and return the text result.

    If the tool call errors (result.is_error), raise ValueError with the
    error text instead of returning it silently.

    TODO: implement this.
    """
    raise NotImplementedError
