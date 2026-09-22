"""The one interface every LLM provider (real or mock) implements.

Lab code depends only on this abstract class, never on a specific vendor SDK, so
swapping providers is a one-line change. See shared/llm/client.py for the factory
that picks a concrete implementation from an env var or explicit name.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from shared.llm.types import CompletionResponse, Message, StreamChunk, ToolDefinition


class LLMProvider(ABC):
    @abstractmethod
    async def complete(
        self,
        messages: list[Message],
        *,
        model: str,
        tools: list[ToolDefinition] | None = None,
        max_tokens: int = 1024,
        temperature: float = 1.0,
        response_schema: dict | None = None,
    ) -> CompletionResponse:
        """Send messages, get one complete response back (no streaming)."""

    @abstractmethod
    def stream(
        self,
        messages: list[Message],
        *,
        model: str,
        tools: list[ToolDefinition] | None = None,
        max_tokens: int = 1024,
        temperature: float = 1.0,
    ) -> AsyncIterator[StreamChunk]:
        """Send messages, get an async stream of chunks back."""
