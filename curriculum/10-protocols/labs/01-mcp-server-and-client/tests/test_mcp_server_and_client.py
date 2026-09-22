import pytest
from mcp import Client


async def test_list_available_tools(server_module, client_module):
    async with Client(server_module.mcp) as mcp_client:
        names = await client_module.list_available_tools(mcp_client)

    assert set(names) == {"calculate", "get_weather"}


async def test_call_calculate_returns_correct_result(server_module, client_module):
    async with Client(server_module.mcp) as mcp_client:
        result = await client_module.call_calculate(mcp_client, "2 + 2 * 3")

    assert result == 8


async def test_call_get_weather_known_city(server_module, client_module):
    async with Client(server_module.mcp) as mcp_client:
        result = await client_module.call_get_weather(mcp_client, "Paris")

    assert "cloudy" in result.lower() or "18" in result


async def test_call_get_weather_unknown_city_raises(server_module, client_module):
    async with Client(server_module.mcp) as mcp_client:
        with pytest.raises(ValueError):
            await client_module.call_get_weather(mcp_client, "Atlantis")


async def test_server_tool_descriptions_are_not_empty(server_module):
    async with Client(server_module.mcp) as mcp_client:
        tools = await mcp_client.list_tools()

    for tool in tools.tools:
        assert tool.description
        assert len(tool.description) > 5
