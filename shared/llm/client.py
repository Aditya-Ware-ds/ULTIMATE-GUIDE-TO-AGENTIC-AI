"""The single entry point labs use to get an LLM client.

Labs call `get_client()` and never import a vendor SDK or a specific provider class
directly. This is what makes the curriculum provider-agnostic: swapping providers
is an env var change (LLM_PROVIDER=anthropic|openai|gemini|ollama|mock), not a code
change.
"""

from __future__ import annotations

import os
from collections.abc import AsyncIterator

from shared.llm.base import LLMProvider
from shared.llm.mock import MockLLMProvider
from shared.llm.types import CompletionResponse, Message, StreamChunk, ToolDefinition


class LLMClient:
    """Thin wrapper around a provider that adds default-model handling."""

    def __init__(self, provider: LLMProvider, default_model: str) -> None:
        self.provider = provider
        self.default_model = default_model

    async def complete(
        self,
        messages: list[Message],
        *,
        model: str | None = None,
        tools: list[ToolDefinition] | None = None,
        max_tokens: int = 1024,
        temperature: float = 1.0,
        response_schema: dict | None = None,
    ) -> CompletionResponse:
        return await self.provider.complete(
            messages,
            model=model or self.default_model,
            tools=tools,
            max_tokens=max_tokens,
            temperature=temperature,
            response_schema=response_schema,
        )

    def stream(
        self,
        messages: list[Message],
        *,
        model: str | None = None,
        tools: list[ToolDefinition] | None = None,
        max_tokens: int = 1024,
        temperature: float = 1.0,
    ) -> AsyncIterator[StreamChunk]:
        return self.provider.stream(
            messages,
            model=model or self.default_model,
            tools=tools,
            max_tokens=max_tokens,
            temperature=temperature,
        )


_DEFAULT_MODELS = {
    "anthropic": "claude-haiku-4-5",
    "openai": "gpt-5-nano",
    "gemini": "gemini-3-flash",
    "ollama": "qwen3:8b",
    "mock": "mock-model",
}


def get_client(provider: str | None = None, *, model: str | None = None) -> LLMClient:
    """Build an LLMClient. `provider` defaults to the LLM_PROVIDER env var, then "mock".

    Every lab's test suite uses provider="mock" (or leaves LLM_PROVIDER unset) so it
    runs with no API keys and no network access.
    """
    provider_name = provider or os.environ.get("LLM_PROVIDER", "mock")
    default_model = model or _DEFAULT_MODELS.get(provider_name, "mock-model")

    if provider_name == "mock":
        return LLMClient(MockLLMProvider(), default_model)
    if provider_name == "anthropic":
        from shared.llm.providers.anthropic_provider import AnthropicProvider

        return LLMClient(AnthropicProvider(), default_model)
    if provider_name == "openai":
        from shared.llm.providers.openai_provider import OpenAIProvider

        return LLMClient(OpenAIProvider(), default_model)
    if provider_name == "gemini":
        from shared.llm.providers.gemini_provider import GeminiProvider

        return LLMClient(GeminiProvider(), default_model)
    if provider_name == "ollama":
        from shared.llm.providers.ollama_provider import OllamaProvider

        return LLMClient(OllamaProvider(), default_model)
    raise ValueError(
        f"Unknown provider {provider_name!r}. Use one of: mock, anthropic, openai, gemini, ollama."
    )
