"""Adapter for Google's Gemini API via the google-genai SDK's Interactions API,
which is the current standard as of 2026 (superseding the older generate_content
flow for new tool-calling integrations).

Verified against https://ai.google.dev/gemini-api/docs/function-calling on
2026-09-22. Only exercised by `live`-marked tests -- re-check that URL if this stops
working. Native token-level streaming for the Interactions API was not clearly
documented at verification time, so `stream()` here is a non-native fallback that
calls complete() once and re-chunks the text; replace with real streaming once the
SDK's streaming shape for interactions.create is confirmed (tracked in PROGRESS.md).
"""

from __future__ import annotations

import json
from collections.abc import AsyncIterator

from shared.llm.base import LLMProvider
from shared.llm.types import (
    CompletionResponse,
    Message,
    Role,
    StreamChunk,
    ToolCall,
    ToolDefinition,
    Usage,
)


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str | None = None) -> None:
        try:
            from google import genai
        except ImportError as exc:  # pragma: no cover
            raise ImportError("Install the 'google-genai' package to use GeminiProvider") from exc
        self._client = genai.Client(api_key=api_key) if api_key else genai.Client()

    @staticmethod
    def _to_wire(messages: list[Message]) -> tuple[list[dict], str | None]:
        """Returns (input items, previous system instruction) -- Gemini's Interactions
        API takes a flat input list plus optional system_instruction, not a role list.
        """
        wire: list[dict] = []
        system: str | None = None
        for m in messages:
            if m.role == Role.SYSTEM:
                system = m.content
                continue
            if m.role == Role.TOOL and m.tool_result:
                wire.append(
                    {
                        "type": "function_result",
                        "name": "",
                        "call_id": m.tool_result.tool_call_id,
                        "result": [{"type": "text", "text": m.tool_result.content}],
                    }
                )
                continue
            if m.tool_calls:
                continue  # the model's own prior tool calls aren't re-sent as input
            wire.append({"role": m.role.value, "content": m.content or ""})
        return wire, system

    @staticmethod
    def _tool_defs(tools: list[ToolDefinition] | None) -> list[dict] | None:
        if not tools:
            return None
        return [
            {
                "type": "function",
                "name": t.name,
                "description": t.description,
                "parameters": t.parameters,
            }
            for t in tools
        ]

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
        wire_input, system = self._to_wire(messages)
        kwargs: dict = {"model": model, "input": wire_input}
        if system:
            kwargs["system_instruction"] = system
        tool_defs = self._tool_defs(tools)
        if tool_defs:
            kwargs["tools"] = tool_defs
        interaction = await self._client.aio.interactions.create(**kwargs)
        steps = getattr(interaction, "steps", [])
        tool_calls = [
            ToolCall(
                id=s.id,
                name=s.name,
                arguments=json.loads(s.arguments) if isinstance(s.arguments, str) else s.arguments,
            )
            for s in steps
            if getattr(s, "type", None) == "function_call"
        ]
        text = getattr(interaction, "output_text", None)
        message = Message(role=Role.ASSISTANT, content=text or None, tool_calls=tool_calls)
        usage_meta = getattr(interaction, "usage", None)
        usage = Usage(
            input_tokens=getattr(usage_meta, "input_tokens", 0) or 0,
            output_tokens=getattr(usage_meta, "output_tokens", 0) or 0,
        )
        finish_reason = "tool_calls" if tool_calls else "stop"
        return CompletionResponse(
            message=message, usage=usage, model=model, finish_reason=finish_reason, raw=interaction
        )

    async def stream(
        self,
        messages: list[Message],
        *,
        model: str,
        tools: list[ToolDefinition] | None = None,
        max_tokens: int = 1024,
        temperature: float = 1.0,
    ) -> AsyncIterator[StreamChunk]:
        response = await self.complete(
            messages, model=model, tools=tools, max_tokens=max_tokens, temperature=temperature
        )
        text = response.message.content or ""
        for i, word in enumerate(text.split(" ")):
            yield StreamChunk(delta=word if i == 0 else f" {word}")
        for tool_call in response.message.tool_calls:
            yield StreamChunk(tool_call=tool_call)
        yield StreamChunk(done=True)
