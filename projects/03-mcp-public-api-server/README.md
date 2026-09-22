# Project 03 -- MCP server for a real public API

**Difficulty:** ★★★☆☆ · **Time estimate:** 1-2 hours
**Comes after:** Level 3, Module 10 (Protocols)

## Spec

Build a real MCP server (Module 10's `mcp.server.MCPServer`, not a toy) that
wraps [Open-Meteo](https://open-meteo.com/en/docs), a free weather-forecast
API that requires no API key for non-commercial use (verified 2026-09-22).
The server exposes one tool, `get_current_weather(latitude, longitude)`,
that calls the real HTTP API and returns a simplified result.

This is an integration project: it reuses Module 10's exact MCP server
pattern (`@mcp.tool()`, in-process `Client(mcp)` testing) against a real
external HTTP API instead of the module's local, in-memory tools. No API key
needed for the default offline tests -- they run against a tiny local HTTP
server shaped like Open-Meteo's real response (same technique as Module 00's
async-fetch-cli lab), not the real internet. One `@pytest.mark.live` test
hits the real API for real, gated per Ground Rule 3 and not run by default.

## Files

- `starter/server.py` -- skeleton with the pieces to implement
- `solution/server.py` -- complete reference implementation
- `tests/` -- offline tests (local fake server) + one live-gated test

## Requirements

Implement these in `starter/server.py`:

- `async def fetch_current_weather(latitude: float, longitude: float) -> dict`
  -- `GET _base_url()` with query params `latitude`, `longitude`, and
  `current="temperature_2m,wind_speed_10m"` via `httpx.AsyncClient`, call
  `response.raise_for_status()`, and return the parsed JSON body.
- `@mcp.tool() async def get_current_weather(latitude: float, longitude: float) -> dict[str, float | str]`
  -- call `fetch_current_weather`, then return
  `{"time": ..., "temperature_c": ..., "wind_speed_kmh": ...}` pulled out of
  the response's `"current"` object (`temperature_2m` -> `temperature_c`,
  `wind_speed_10m` -> `wind_speed_kmh`).

`_base_url()` (already implemented) reads the `OPEN_METEO_BASE_URL` env var
at call time, defaulting to the real Open-Meteo endpoint -- this is what lets
tests point the tool at a local fake server without changing the tool's
public signature.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/server.py`.
- `fetch_current_weather` raises on a non-2xx HTTP response (via
  `raise_for_status`), rather than returning a malformed result.
- `get_current_weather` is registered on `mcp` with a non-empty description
  and returns exactly the three simplified fields, not the raw API response.
- The live test (`-m live`) passes against the real API when you have
  network access.

## Running the tests

```bash
uv run pytest projects/03-mcp-public-api-server/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest projects/03-mcp-public-api-server/tests
```

Live, against the real API:

```bash
uv run pytest -m live projects/03-mcp-public-api-server/tests
```

## Next

[Project 04 -- Multi-agent content pipeline](../04-multi-agent-content-pipeline/README.md)
