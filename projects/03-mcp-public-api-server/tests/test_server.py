import pytest
from mcp import Client


async def test_fetch_current_weather_parses_local_server_response(server_module, local_open_meteo):
    data = await server_module.fetch_current_weather(48.85, 2.35)

    assert data["current"]["temperature_2m"] == 18.4


async def test_get_current_weather_tool_returns_simplified_shape(server_module, local_open_meteo):
    async with Client(server_module.mcp) as mcp_client:
        result = await mcp_client.call_tool(
            "get_current_weather", {"latitude": 48.85, "longitude": 2.35}
        )

    assert result.structured_content == {
        "time": "2026-09-22T12:00",
        "temperature_c": 18.4,
        "wind_speed_kmh": 11.2,
    }


async def test_server_tool_is_registered_with_a_description(server_module, local_open_meteo):
    async with Client(server_module.mcp) as mcp_client:
        tools = await mcp_client.list_tools()

    names = {t.name for t in tools.tools}
    assert "get_current_weather" in names
    tool = next(t for t in tools.tools if t.name == "get_current_weather")
    assert tool.description
    assert len(tool.description) > 5


@pytest.mark.live
async def test_fetch_current_weather_against_the_real_api(server_module):
    """Requires network access to api.open-meteo.com. Run explicitly with:
    uv run pytest -m live projects/03-mcp-public-api-server/tests
    """
    data = await server_module.fetch_current_weather(48.8566, 2.3522)  # Paris

    assert "current" in data
    assert isinstance(data["current"]["temperature_2m"], int | float)
