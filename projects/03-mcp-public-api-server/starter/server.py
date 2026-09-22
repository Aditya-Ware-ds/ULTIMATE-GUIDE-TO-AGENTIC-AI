"""Project 03: MCP server wrapping the Open-Meteo forecast API.
See ../README.md for the full spec.

Verified against https://open-meteo.com/en/docs on 2026-09-22: no API key
required for non-commercial use.
"""

from __future__ import annotations

import os

import httpx  # noqa: F401 -- used once you implement fetch_current_weather below
from mcp.server import MCPServer

mcp = MCPServer("public-api-tools")

_DEFAULT_BASE_URL = "https://api.open-meteo.com/v1/forecast"


def _base_url() -> str:
    return os.environ.get("OPEN_METEO_BASE_URL", _DEFAULT_BASE_URL)


async def fetch_current_weather(latitude: float, longitude: float) -> dict:
    """GET `_base_url()` with `latitude`, `longitude`, and
    `current=temperature_2m,wind_speed_10m` query params, raise on a non-2xx
    response, and return the parsed JSON body.

    TODO: implement this.
    """
    raise NotImplementedError


@mcp.tool()
async def get_current_weather(latitude: float, longitude: float) -> dict[str, float | str]:
    """Get the current temperature (Celsius) and wind speed (km/h) for a
    location, given its latitude and longitude.

    Call fetch_current_weather, then return
    {"time": ..., "temperature_c": ..., "wind_speed_kmh": ...} pulled out of
    the response's "current" object.

    TODO: implement this.
    """
    raise NotImplementedError


if __name__ == "__main__":
    mcp.run()
