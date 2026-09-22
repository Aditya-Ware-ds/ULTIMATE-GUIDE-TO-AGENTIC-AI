import pytest

from shared.llm.mock import MockLLMProvider
from shared.llm.types import Message, Role


async def test_add_text_returns_scripted_response():
    provider = MockLLMProvider()
    provider.add_text("hello there")

    response = await provider.complete([Message(role=Role.USER, content="hi")])

    assert response.message.content == "hello there"
    assert response.finish_reason == "stop"
    assert provider.call_count == 1


async def test_add_tool_call_returns_tool_call():
    provider = MockLLMProvider()
    provider.add_tool_call("get_weather", {"city": "Paris"})

    response = await provider.complete([Message(role=Role.USER, content="weather?")])

    assert response.finish_reason == "tool_calls"
    assert len(response.message.tool_calls) == 1
    assert response.message.tool_calls[0].name == "get_weather"
    assert response.message.tool_calls[0].arguments == {"city": "Paris"}


async def test_multiple_scripted_turns_are_consumed_in_order():
    provider = MockLLMProvider()
    provider.add_tool_call("search", {"query": "x"})
    provider.add_text("final answer")

    first = await provider.complete([Message(role=Role.USER, content="q")])
    second = await provider.complete([Message(role=Role.USER, content="q")])

    assert first.message.tool_calls[0].name == "search"
    assert second.message.content == "final answer"
    assert provider.exhausted


async def test_raises_when_script_exhausted():
    provider = MockLLMProvider()

    with pytest.raises(AssertionError):
        await provider.complete([Message(role=Role.USER, content="hi")])


async def test_stream_yields_text_then_done():
    provider = MockLLMProvider()
    provider.add_text("hello world")

    chunks = [chunk async for chunk in provider.stream([Message(role=Role.USER, content="hi")])]

    assert "".join(c.delta for c in chunks) == "hello world"
    assert chunks[-1].done is True
