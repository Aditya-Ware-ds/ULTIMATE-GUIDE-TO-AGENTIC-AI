import json

import jsonschema
import pytest

from shared.llm.types import Role, Usage

SCHEMA = {
    "type": "object",
    "properties": {"city": {"type": "string"}, "country": {"type": "string"}},
    "required": ["city", "country"],
}


def test_build_messages_includes_system_prompt_first(chat):
    messages = chat.build_messages("Be concise.", [])

    assert messages[0].role == Role.SYSTEM
    assert messages[0].content == "Be concise."


def test_build_messages_maps_history_roles(chat):
    history = [("user", "Hi"), ("assistant", "Hello")]

    messages = chat.build_messages("system", history)

    assert [m.role for m in messages[1:]] == [Role.USER, Role.ASSISTANT]
    assert [m.content for m in messages[1:]] == ["Hi", "Hello"]


async def test_chat_once_returns_reply_and_updates_history(chat, client):
    client.provider.add_text("4")
    history: list[tuple[str, str]] = []

    reply = await chat.chat_once(client, "Be concise.", history, "What's 2+2?")

    assert reply == "4"
    assert history == [("user", "What's 2+2?"), ("assistant", "4")]


async def test_chat_once_second_call_sees_full_history(chat, client):
    client.provider.add_text("4")
    client.provider.add_text("40")
    history: list[tuple[str, str]] = []

    await chat.chat_once(client, "Be concise.", history, "What's 2+2?")
    await chat.chat_once(client, "Be concise.", history, "And that times 10?")

    second_call_messages = client.provider.calls[1]["messages"]
    contents = [m.content for m in second_call_messages]
    assert "What's 2+2?" in contents
    assert "4" in contents
    assert "And that times 10?" in contents


async def test_extract_structured_returns_valid_dict(chat, client):
    client.provider.add_text('{"city": "Paris", "country": "France"}')

    result = await chat.extract_structured(client, "I live in Paris, France.", SCHEMA)

    assert result == {"city": "Paris", "country": "France"}


async def test_extract_structured_raises_on_schema_violation(chat, client):
    client.provider.add_text('{"city": "Paris"}')  # missing required "country"

    with pytest.raises(jsonschema.ValidationError):
        await chat.extract_structured(client, "...", SCHEMA)


async def test_extract_structured_raises_on_malformed_json(chat, client):
    client.provider.add_text("not valid json")

    with pytest.raises(json.JSONDecodeError):
        await chat.extract_structured(client, "...", SCHEMA)


async def test_stream_and_collect_matches_complete(chat, client):
    from shared.llm.types import Message

    client.provider.add_text("hello world")
    messages = [Message(role=Role.USER, content="hi")]

    result = await chat.stream_and_collect(client, messages)

    assert result == "hello world"


def test_estimate_call_cost_matches_pricing_table(chat):
    usage = Usage(input_tokens=1_000_000, output_tokens=1_000_000)

    from shared.llm.pricing import PRICING

    cost = chat.estimate_call_cost("openai", usage)

    price = PRICING["openai"]
    assert cost == pytest.approx(price.input_per_million + price.output_per_million)
