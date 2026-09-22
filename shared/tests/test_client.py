import pytest

from shared.llm.client import get_client
from shared.llm.mock import MockLLMProvider
from shared.llm.types import Message, Role


async def test_get_client_defaults_to_mock(monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER", raising=False)

    client = get_client()

    assert isinstance(client.provider, MockLLMProvider)
    assert client.default_model == "mock-model"


async def test_get_client_reads_env_var(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")

    client = get_client()

    assert isinstance(client.provider, MockLLMProvider)


async def test_client_complete_delegates_to_provider():
    client = get_client("mock")
    client.provider.add_text("hi back")

    response = await client.complete([Message(role=Role.USER, content="hi")])

    assert response.message.content == "hi back"


async def test_unknown_provider_raises():
    with pytest.raises(ValueError):
        get_client("not-a-real-provider")


async def test_explicit_model_overrides_default():
    client = get_client("mock", model="my-model")
    client.provider.add_text("ok")

    response = await client.complete(
        [Message(role=Role.USER, content="hi")], model="override-model"
    )

    assert response.model == "override-model"
