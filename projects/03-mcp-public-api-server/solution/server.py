"""Project 03: MCP server wrapping the Open-Meteo forecast API -- reference
solution. See ../README.md.

Verified against https://open-meteo.com/en/docs on 2026-09-22: no API key
required for non-commercial use; `GET {BASE_URL}?latitude=..&longitude=..
&current=temperature_2m,wind_speed_10m` returns
`{"current": {"time": ..., "temperature_2m": ..., "wind_speed_10m": ...}}`.
"""

from __future__ import annotations

import os

import httpx
from mcp.server import MCPServer

mcp = MCPServer("public-api-tools")

_DEFAULT_BASE_URL = "https://api.open-meteo.com/v1/forecast"


def _base_url() -> str:
    # Read at call time (not at import time) so tests can point this at a
    # local fake server instead of the real internet (see
    # tests/conftest.py's `local_server` fixture) -- the same idea as
    # Module 00's async-fetch-cli lab, adapted for a fixed tool signature
    # that can't take an arbitrary URL argument.
    return os.environ.get("OPEN_METEO_BASE_URL", _DEFAULT_BASE_URL)


async def fetch_current_weather(latitude: float, longitude: float) -> dict:
    async with httpx.AsyncClient() as http_client:
        response = await http_client.get(
            _base_url(),
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,wind_speed_10m",
            },
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_current_weather(latitude: float, longitude: float) -> dict[str, float | str]:
    """Get the current temperature (Celsius) and wind speed (km/h) for a
    location, given its latitude and longitude."""
    data = await fetch_current_weather(latitude, longitude)
    current = data["current"]
    return {
        "time": current["time"],
        "temperature_c": current["temperature_2m"],
        "wind_speed_kmh": current["wind_speed_10m"],
    }


if __name__ == "__main__":
    mcp.run()
