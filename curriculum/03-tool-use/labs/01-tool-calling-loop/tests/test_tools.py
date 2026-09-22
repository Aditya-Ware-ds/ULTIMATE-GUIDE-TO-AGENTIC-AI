import pytest

from shared.llm.types import ToolCall


def test_calculate_basic_arithmetic(tools):
    assert tools.calculate("2 + 2") == 4
    assert tools.calculate("2 + 2 * 3") == 8
    assert tools.calculate("(2 + 3) * 4") == 20
    assert tools.calculate("10 / 4") == 2.5
    assert tools.calculate("-5 + 2") == -3


def test_calculate_rejects_non_arithmetic(tools):
    with pytest.raises(ValueError):
        tools.calculate("__import__('os')")

    with pytest.raises(ValueError):
        tools.calculate("'a string'")

    with pytest.raises(ValueError):
        tools.calculate("not valid syntax +++")


def test_calculate_division_by_zero_raises(tools):
    with pytest.raises(Exception):  # noqa: B017 -- ZeroDivisionError or ValueError, either is fine
        tools.calculate("1 / 0")


def test_get_weather_known_city(tools):
    result = tools.get_weather("Paris")

    assert result["city"] == "Paris"
    assert "condition" in result
    assert result["unit"] == "celsius"


def test_get_weather_fahrenheit_conversion(tools):
    celsius_result = tools.get_weather("Tokyo", unit="celsius")
    fahrenheit_result = tools.get_weather("Tokyo", unit="fahrenheit")

    assert fahrenheit_result["temperature"] != celsius_result["temperature"]


def test_get_weather_unknown_city_raises(tools):
    with pytest.raises(ValueError):
        tools.get_weather("Atlantis")


def test_tool_definitions_cover_both_tools(tools):
    names = {t.name for t in tools.TOOL_DEFINITIONS}
    assert names == {"calculate", "get_weather"}


def test_tool_registry_matches_definitions(tools):
    definition_names = {t.name for t in tools.TOOL_DEFINITIONS}
    assert definition_names == {"calculate", "get_weather"}
    assert set(tools.TOOL_REGISTRY.keys()) == definition_names


def test_dispatch_success(tools):
    call = ToolCall(id="1", name="calculate", arguments={"expression": "2 + 2"})

    result = tools.dispatch(call, tools.TOOL_REGISTRY)

    assert not result.is_error
    assert result.content == "4"
    assert result.tool_call_id == "1"


def test_dispatch_unknown_tool_does_not_raise(tools):
    call = ToolCall(id="2", name="not_a_real_tool", arguments={})

    result = tools.dispatch(call, tools.TOOL_REGISTRY)

    assert result.is_error
    assert "not_a_real_tool" in result.content


def test_dispatch_execution_error_does_not_raise(tools):
    call = ToolCall(id="3", name="get_weather", arguments={"city": "Atlantis"})

    result = tools.dispatch(call, tools.TOOL_REGISTRY)

    assert result.is_error
    assert result.tool_call_id == "3"


async def test_run_tool_loop_single_tool_call(tools, client):
    client.provider.add_tool_call("get_weather", {"city": "Paris"})
    client.provider.add_text("It's cloudy in Paris.")

    result = await tools.run_tool_loop(client, "Be concise.", "What's the weather in Paris?")

    assert result == "It's cloudy in Paris."


async def test_run_tool_loop_multi_step(tools, client):
    client.provider.add_tool_call("calculate", {"expression": "2 + 2"})
    client.provider.add_tool_call("get_weather", {"city": "Tokyo"})
    client.provider.add_text("2+2 is 4, and Tokyo is sunny.")

    result = await tools.run_tool_loop(client, "Be concise.", "What's 2+2, and weather in Tokyo?")

    assert result == "2+2 is 4, and Tokyo is sunny."
    assert client.provider.call_count == 3


async def test_run_tool_loop_stops_at_max_steps(tools, client):
    for _ in range(10):
        client.provider.add_tool_call("calculate", {"expression": "1 + 1"})

    result = await tools.run_tool_loop(
        client, "Be concise.", "Keep calculating forever.", max_steps=3
    )

    assert "max steps" in result.lower() or "3" in result
    assert client.provider.call_count == 3
